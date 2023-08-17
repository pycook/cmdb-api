# -*- coding:utf-8 -*-


import copy
import datetime
import json

from flask import abort
from flask import current_app
from flask_login import current_user
from werkzeug.exceptions import BadRequest

from api.extensions import db
from api.extensions import rd
from api.lib.cmdb.cache import AttributeCache
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci_type import CITypeAttributeManager
from api.lib.cmdb.ci_type import CITypeManager
from api.lib.cmdb.ci_type import CITypeRelationManager
from api.lib.cmdb.ci_type import CITypeUniqueConstraintManager
from api.lib.cmdb.const import AttributeDefaultValueEnum
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import ConstraintEnum
from api.lib.cmdb.const import ExistPolicy
from api.lib.cmdb.const import OperateType
from api.lib.cmdb.const import PermEnum, ResourceTypeEnum
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import RetKey
from api.lib.cmdb.history import AttributeHistoryManger
from api.lib.cmdb.history import CIRelationHistoryManager
from api.lib.cmdb.perms import CIFilterPermsCRUD
from api.lib.cmdb.resp_format import ErrFormat
from api.lib.cmdb.utils import TableMap
from api.lib.cmdb.utils import ValueTypeMap
from api.lib.cmdb.value import AttributeValueManager
from api.lib.decorator import kwargs_required
from api.lib.perm.acl.acl import ACLManager
from api.lib.perm.acl.acl import is_app_admin
from api.lib.perm.acl.acl import validate_permission
from api.lib.utils import Lock
from api.lib.utils import handle_arg_list
from api.models.cmdb import CI
from api.models.cmdb import CIRelation
from api.models.cmdb import CITypeAttribute
from api.models.cmdb import CITypeRelation
from api.tasks.cmdb import ci_cache
from api.tasks.cmdb import ci_delete
from api.tasks.cmdb import ci_relation_cache
from api.tasks.cmdb import ci_relation_delete

PRIVILEGED_USERS = {"worker", "cmdb_agent", "agent"}


class CIManager(object):
    """ manage CI interface
    """

    def __init__(self):
        pass

    @staticmethod
    def get_by_id(ci_id):
        return CI.get_by_id(ci_id)

    @staticmethod
    def get_type_name(ci_id):
        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))
        return CITypeCache.get(ci.type_id).name

    @staticmethod
    def get_type(ci_id):
        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))
        return CITypeCache.get(ci.type_id)

    @staticmethod
    def confirm_ci_existed(ci_id):
        return CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

    @classmethod
    def get_ci_by_id(cls, ci_id, ret_key=RetKey.NAME, fields=None, need_children=True):
        """

        :param ci_id:
        :param ret_key: name, id, or alias
        :param fields:  attribute list
        :param need_children:
        :return:
        """

        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        res = dict()

        if need_children:
            children = CIRelationManager.get_children(ci_id, ret_key=ret_key)  # one floor
            res.update(children)

        ci_type = CITypeCache.get(ci.type_id)
        res["ci_type"] = ci_type.name

        res.update(cls.get_cis_by_ids([str(ci_id)], fields=fields, ret_key=ret_key))

        res['_type'] = ci_type.id
        res['_id'] = ci_id

        return res

    @classmethod
    def valid_ci_only_read(cls, ci):
        if is_app_admin("cmdb"):
            return

        validate_permission(CIManager.get_type_name(ci.id), ResourceTypeEnum.CI, PermEnum.READ, "cmdb")

        acl = ACLManager('cmdb')
        res = acl.get_resources(ResourceTypeEnum.CI_FILTER)

        if res and ci.type_id in CIFilterPermsCRUD().get_by_ids(list(map(int, [i['name'] for i in res]))):
            return abort(403, ErrFormat.no_permission2)

    @classmethod
    def _valid_ci_for_no_read(cls, ci, ci_type=None):
        type_id = ci.type_id if ci else ci_type.id

        acl = ACLManager('cmdb')
        res = acl.get_resources(ResourceTypeEnum.CI_FILTER)

        type2filters = CIFilterPermsCRUD().get_by_ids(list(map(int, [i['name'] for i in res])), type_id=type_id)
        if res and type_id in type2filters:
            if type2filters[type_id].get('ci_filter') and ci:
                from api.lib.cmdb.search import SearchError
                from api.lib.cmdb.search.ci import search

                query = "_id:{},{}".format(ci.id, type2filters[type_id].get('ci_filter'))
                s = search(query)
                try:
                    response, _, _, _, _, _ = s.search()
                except SearchError as e:
                    current_app.logger.warning(e)
                    return abort(400, str(e))

                if not response:
                    return abort(403, ErrFormat.ci_filter_perm_ci_no_permission)

            return type2filters[type_id].get('attr_filter') or []

    @classmethod
    def get_ci_by_id_from_db(cls, ci_id, ret_key=RetKey.NAME, fields=None, need_children=True, use_master=False,
                             valid=False):
        """

        :param ci_id:
        :param ret_key: name, id or alias
        :param fields: list
        :param need_children:
        :param use_master: whether to use master db
        :param valid:
        :return:
        """

        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        if valid:
            cls.valid_ci_only_read(ci)

        res = dict()

        if need_children:
            children = CIRelationManager.get_children(ci_id, ret_key=ret_key)  # one floor
            res.update(children)

        ci_type = CITypeCache.get(ci.type_id)
        res["ci_type"] = ci_type.name

        fields = CITypeAttributeManager.get_attr_names_by_type_id(ci.type_id) if not fields else fields
        unique_key = AttributeCache.get(ci_type.unique_id)
        _res = AttributeValueManager().get_attr_values(fields,
                                                       ci_id,
                                                       ret_key=ret_key,
                                                       unique_key=unique_key,
                                                       use_master=use_master)
        res.update(_res)

        res['_type'] = ci_type.id
        res['ci_type_alias'] = ci_type.alias
        res['_id'] = ci_id

        return res

    def get_ci_by_ids(self, ci_id_list, ret_key=RetKey.NAME, fields=None):
        return [self.get_ci_by_id(ci_id, ret_key=ret_key, fields=fields) for ci_id in ci_id_list]

    @classmethod
    def get_cis_by_type(cls, type_id, ret_key=RetKey.NAME, fields="", page=1, per_page=None):
        cis = db.session.query(CI.id).filter(CI.type_id == type_id).filter(CI.deleted.is_(False))
        numfound = cis.count()

        cis = cis.offset((page - 1) * per_page).limit(per_page)
        ci_ids = [str(ci.id) for ci in cis]
        res = cls.get_cis_by_ids(ci_ids, ret_key, fields)

        return numfound, page, res

    @classmethod
    def get_ad_statistics(cls):
        res = CI.get_by(to_dict=False)
        result = dict()
        for i in res:
            result.setdefault(i.type_id, dict(total=0, auto_discovery=0))
            result[i.type_id]['total'] += 1
            if i.is_auto_discovery:
                result[i.type_id]['auto_discovery'] += 1

        return result

    @staticmethod
    def ci_is_exist(unique_key, unique_value, type_id):
        """

        :param unique_key: is a attribute
        :param unique_value:
        :param type_id:
        :return:
        """
        value_table = TableMap(attr=unique_key).table

        unique = db.session.query(value_table).join(CI, CI.id == value_table.ci_id).filter(
            value_table.attr_id == unique_key.id).filter(value_table.value == unique_value).filter(
            CI.type_id == type_id).filter(CI.deleted.is_(False)).filter(value_table.deleted.is_(False)).first()

        if unique:
            return CI.get_by_id(unique.ci_id)

    @staticmethod
    def _delete_ci_by_id(ci_id, soft_delete=False):
        ci = CI.get_by_id(ci_id)
        if soft_delete:
            ci.soft_delete()
        else:
            ci.delete()

    @staticmethod
    def _valid_unique_constraint(type_id, ci_dict, ci_id=None):
        unique_constraints = CITypeUniqueConstraintManager.get_by_type_id(type_id)
        if not unique_constraints:
            return

        attr_ids = []
        for i in unique_constraints:
            attr_ids.extend(i.attr_ids)

        attrs = [AttributeCache.get(i) for i in list(set(attr_ids))]
        id2name = {i.id: i.name for i in attrs if i}
        not_existed_fields = list(set(id2name.values()) - set(ci_dict.keys()))
        if not_existed_fields and ci_id is not None:
            ci_dict = copy.deepcopy(ci_dict)
            ci_dict.update(AttributeValueManager().get_attr_values(not_existed_fields, ci_id))

        for constraint in unique_constraints:
            ci_ids = None
            for attr_id in constraint.attr_ids:
                value_table = TableMap(attr_name=id2name[attr_id]).table

                _ci_ids = set([i.ci_id for i in value_table.get_by(attr_id=attr_id,
                                                                   to_dict=False,
                                                                   value=ci_dict.get(id2name[attr_id]) or None)])
                if ci_ids is None:
                    ci_ids = _ci_ids
                else:
                    ci_ids &= _ci_ids

            if ci_ids - (ci_id and {ci_id} or set()):
                return abort(400, ErrFormat.unique_constraint.format(
                    " - ".join([id2name[i] for i in constraint.attr_ids])))

    @staticmethod
    def _auto_inc_id(attr):
        db.session.remove()

        value_table = TableMap(attr_name=attr.name).table
        with Lock("auto_inc_id_{}".format(attr.name), need_lock=True):
            max_v = value_table.get_by(attr_id=attr.id, only_query=True).order_by(
                getattr(value_table, 'value').desc()).first()
            if max_v is not None:
                return int(max_v.value) + 1

            return 1

    @classmethod
    def add(cls, ci_type_name,
            exist_policy=ExistPolicy.REPLACE,
            _no_attribute_policy=ExistPolicy.IGNORE,
            is_auto_discovery=False,
            _is_admin=False,
            **ci_dict):
        """

        :param ci_type_name:
        :param exist_policy: replace or reject or need
        :param _no_attribute_policy: ignore or reject
        :param is_auto_discovery: default is False
        :param _is_admin: default is False
        :param ci_dict:
        :return:
        """
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ci_type = CITypeManager.check_is_existed(ci_type_name)

        unique_key = AttributeCache.get(ci_type.unique_id) or abort(
            400, ErrFormat.unique_value_not_found.format("unique_id={}".format(ci_type.unique_id)))

        unique_value = ci_dict.get(unique_key.name)
        unique_value = unique_value or ci_dict.get(unique_key.alias)
        unique_value = unique_value or ci_dict.get(unique_key.id)
        unique_value = unique_value or abort(400, ErrFormat.unique_key_required.format(unique_key.name))

        attrs = CITypeAttributesCache.get2(ci_type_name)
        ci_type_attrs_name = {attr.name: attr for _, attr in attrs}
        ci_type_attrs_alias = {attr.alias: attr for _, attr in attrs}
        ci_attr2type_attr = {type_attr.attr_id: type_attr for type_attr, _ in attrs}

        ci = None
        need_lock = current_user.username not in current_app.config.get('PRIVILEGED_USERS', PRIVILEGED_USERS)
        with Lock(ci_type_name, need_lock=need_lock):
            existed = cls.ci_is_exist(unique_key, unique_value, ci_type.id)
            if existed is not None:
                if exist_policy == ExistPolicy.REJECT:
                    return abort(400, ErrFormat.ci_is_already_existed)

                if existed.type_id != ci_type.id:
                    existed.update(type_id=ci_type.id)
                ci = existed
            else:
                if exist_policy == ExistPolicy.NEED:
                    return abort(404, ErrFormat.ci_not_found.format("{}={}".format(unique_key.name, unique_value)))

                from api.lib.cmdb.const import L_CI
                if L_CI and len(CI.get_by(type_id=ci_type.id)) > L_CI * 2:
                    return abort(400, ErrFormat.limit_ci.format(L_CI * 2))

            limit_attrs = cls._valid_ci_for_no_read(ci, ci_type) if not _is_admin else {}

            if existed is None:  # set default
                for type_attr, attr in attrs:
                    if attr.default and attr.default.get('default') is not None:
                        if attr.default.get('default') and attr.default.get('default') in (
                                AttributeDefaultValueEnum.CREATED_AT, AttributeDefaultValueEnum.UPDATED_AT):
                            ci_dict[attr.name] = now
                        elif attr.default.get('default') == AttributeDefaultValueEnum.AUTO_INC_ID:
                            ci_dict[attr.name] = cls._auto_inc_id(attr)
                        elif ((attr.name not in ci_dict and attr.alias not in ci_dict) or (
                                ci_dict.get(attr.name) is None and ci_dict.get(attr.alias) is None)):
                            ci_dict[attr.name] = attr.default.get('default')

                    if type_attr.is_required and (attr.name not in ci_dict and attr.alias not in ci_dict):
                        return abort(400, ErrFormat.attribute_value_required.format(attr.name))
            else:
                for type_attr, attr in attrs:
                    if attr.default and attr.default.get('default') == AttributeDefaultValueEnum.UPDATED_AT:
                        ci_dict[attr.name] = now

            computed_attrs = [attr.to_dict() for _, attr in attrs if attr.is_computed] or None

            value_manager = AttributeValueManager()

            if computed_attrs:
                value_manager.handle_ci_compute_attributes(ci_dict, computed_attrs, ci)

            cls._valid_unique_constraint(ci_type.id, ci_dict, ci and ci.id)

            for k in ci_dict:
                if k not in ci_type_attrs_name and k not in ci_type_attrs_alias and \
                        _no_attribute_policy == ExistPolicy.REJECT:
                    return abort(400, ErrFormat.attribute_not_found.format(k))

                if limit_attrs and ci_type_attrs_name.get(k) not in limit_attrs and \
                        ci_type_attrs_alias.get(k) not in limit_attrs:
                    return abort(403, ErrFormat.ci_filter_perm_attr_no_permission.format(k))

            ci_dict = {k: v for k, v in ci_dict.items() if k in ci_type_attrs_name or k in ci_type_attrs_alias}

            key2attr = value_manager.valid_attr_value(ci_dict, ci_type.id, ci and ci.id,
                                                      ci_type_attrs_name, ci_type_attrs_alias, ci_attr2type_attr)

            try:
                ci = ci or CI.create(type_id=ci_type.id, is_auto_discovery=is_auto_discovery)
                record_id = value_manager.create_or_update_attr_value2(ci, ci_dict, key2attr)
            except BadRequest as e:
                if existed is None:
                    cls.delete(ci.id)
                raise e

        if record_id:  # has change
            ci_cache.apply_async([ci.id], queue=CMDB_QUEUE)

        return ci.id

    def update(self, ci_id, _is_admin=False, **ci_dict):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ci = self.confirm_ci_existed(ci_id)

        attrs = CITypeAttributesCache.get2(ci.type_id)
        ci_type_attrs_name = {attr.name: attr for _, attr in attrs}
        ci_attr2type_attr = {type_attr.attr_id: type_attr for type_attr, _ in attrs}
        for _, attr in attrs:
            if attr.default and attr.default.get('default') == AttributeDefaultValueEnum.UPDATED_AT:
                ci_dict[attr.name] = now

        computed_attrs = [attr.to_dict() for _, attr in attrs if attr.is_computed] or None

        value_manager = AttributeValueManager()

        if computed_attrs:
            value_manager.handle_ci_compute_attributes(ci_dict, computed_attrs, ci)

        limit_attrs = self._valid_ci_for_no_read(ci) if not _is_admin else {}

        need_lock = current_user.username not in current_app.config.get('PRIVILEGED_USERS', PRIVILEGED_USERS)
        with Lock(ci.ci_type.name, need_lock=need_lock):
            self._valid_unique_constraint(ci.type_id, ci_dict, ci_id)

            ci_dict = {k: v for k, v in ci_dict.items() if k in ci_type_attrs_name}
            key2attr = value_manager.valid_attr_value(ci_dict, ci.type_id, ci.id, ci_type_attrs_name,
                                                      ci_attr2type_attr=ci_attr2type_attr)
            if limit_attrs:
                for k in ci_dict:
                    if k not in limit_attrs:
                        return abort(403, ErrFormat.ci_filter_perm_attr_no_permission.format(k))

            try:
                record_id = value_manager.create_or_update_attr_value2(ci, ci_dict, key2attr)
            except BadRequest as e:
                raise e

        if record_id:  # has change
            ci_cache.apply_async([ci_id], queue=CMDB_QUEUE)

    @staticmethod
    def update_unique_value(ci_id, unique_name, unique_value):
        ci = CI.get_by_id(ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        AttributeValueManager().create_or_update_attr_value(unique_name, unique_value, ci)

        ci_cache.apply_async([ci_id], queue=CMDB_QUEUE)

    @classmethod
    def delete(cls, ci_id, soft_delete=False):
        ci = CI.get_by_id(ci_id, not soft_delete) or abort(404, ErrFormat.ci_not_found.format("id={}".format(ci_id)))

        cls._valid_ci_for_no_read(ci)

        ci_dict = cls.get_cis_by_ids([ci_id])
        ci_dict = ci_dict and ci_dict[0]

        attrs = CITypeAttribute.get_by(type_id=ci.type_id, to_dict=False)
        attr_names = set([AttributeCache.get(attr.attr_id).name for attr in attrs])
        for attr_name in attr_names:
            value_table = TableMap(attr_name=attr_name).table
            for item in value_table.get_by(ci_id=ci_id, to_dict=False, deleted=not soft_delete):
                if soft_delete:
                    item.soft_delete()
                else:
                    item.delete()

        for item in CIRelation.get_by(first_ci_id=ci_id, to_dict=False, deleted=not soft_delete):
            ci_relation_delete.apply_async(args=(item.first_ci_id, item.second_ci_id), queue=CMDB_QUEUE)
            if soft_delete:
                item.soft_delete()
            else:
                item.delete()

        for item in CIRelation.get_by(second_ci_id=ci_id, to_dict=False, deleted=not soft_delete):
            ci_relation_delete.apply_async(args=(item.first_ci_id, item.second_ci_id), queue=CMDB_QUEUE)
            if soft_delete:
                item.soft_delete()
            else:
                item.delete()

        if soft_delete:
            ci.soft_delete()
            AttributeHistoryManger.add(None, ci_id, [(None, OperateType.SOFT_DELETE, ci_dict, None)], ci.type_id)
        else:
            ci.delete()
            AttributeHistoryManger.add(None, ci_id, [(None, OperateType.DELETE, ci_dict, None)], ci.type_id)

        ci_delete.apply_async([ci.id], queue=CMDB_QUEUE)

        return ci_id

    @staticmethod
    def add_heartbeat(ci_type, unique_value):
        ci_type = CITypeManager().check_is_existed(ci_type)

        unique_key = AttributeCache.get(ci_type.unique_id)
        value_table = TableMap(attr=unique_key).table

        v = value_table.get_by(attr_id=unique_key.id,
                               value=unique_value,
                               to_dict=False,
                               first=True) \
            or abort(404, ErrFormat.not_found)

        ci = CI.get_by_id(v.ci_id) or abort(404, ErrFormat.ci_not_found.format("id={}".format(v.ci_id)))

        ci.update(heartbeat=datetime.datetime.now())

    @classmethod
    @kwargs_required("type_id", "page")
    def get_heartbeat(cls, **kwargs):
        query = db.session.query(CI.id, CI.heartbeat).filter(CI.deleted.is_(False))

        expire = datetime.datetime.now() - datetime.timedelta(minutes=72)
        type_ids = handle_arg_list(kwargs["type_id"])

        query = query.filter(CI.type_id.in_(type_ids))

        page = kwargs.get("page")
        agent_status = kwargs.get("agent_status")
        if agent_status == -1:
            query = query.filter(CI.heartbeat.is_(None))
        elif agent_status == 0:
            query = query.filter(CI.heartbeat <= expire)
        elif agent_status == 1:
            query = query.filter(CI.heartbeat > expire)

        numfound = query.count()
        per_page_count = current_app.config.get("DEFAULT_PAGE_COUNT")
        cis = query.offset((page - 1) * per_page_count).limit(per_page_count).all()
        ci_ids = [ci.id for ci in cis]
        heartbeat_dict = {}
        for ci in cis:
            if agent_status is not None:
                heartbeat_dict[ci.id] = agent_status
            else:
                if ci.heartbeat is None:
                    heartbeat_dict[ci.id] = -1
                elif ci.heartbeat <= expire:
                    heartbeat_dict[ci.id] = 0
                else:
                    heartbeat_dict[ci.id] = 1
        current_app.logger.debug(heartbeat_dict)
        ci_ids = list(map(str, ci_ids))
        res = cls.get_cis_by_ids(ci_ids, fields=["hostname", "private_ip"])
        result = [(i.get("hostname"), i.get("private_ip")[0], i.get("ci_type"),
                   heartbeat_dict.get(i.get("_id"))) for i in res
                  if i.get("private_ip")]
        return numfound, result

    @staticmethod
    def _get_cis_from_cache(ci_ids, ret_key=RetKey.NAME, fields=None, unique_required=False, excludes=None):
        res = rd.get(ci_ids, REDIS_PREFIX_CI)
        if res is not None and None not in res and ret_key == RetKey.NAME:
            res = list(map(json.loads, res))
            if not fields and not excludes:
                return res
            elif fields:
                _res = []
                for d in res:
                    _d = dict()
                    _d["_id"], _d["_type"] = d.get("_id"), d.get("_type")
                    _d["ci_type"] = d.get("ci_type")
                    if unique_required:
                        _d[d.get('unique')] = d.get(d.get('unique'))

                    for field in fields + ['ci_type_alias', 'unique', 'unique_alias']:
                        _d[field] = d.get(field)
                    _res.append(_d)
                return _res
            else:
                excludes = set(excludes)
                for i in res:
                    for e in excludes:
                        i.pop(e, None)

                return res

    @staticmethod
    def _get_cis_from_db(ci_ids, ret_key=RetKey.NAME, fields=None, value_tables=None, excludes=None):
        from api.lib.cmdb.search.ci.db.query_sql import QUERY_CIS_BY_IDS
        from api.lib.cmdb.search.ci.db.query_sql import QUERY_CIS_BY_VALUE_TABLE

        if not fields:
            filter_fields_sql = ""
        else:
            _fields = list()
            for field in fields:
                attr = AttributeCache.get(field)
                if attr is not None:
                    _fields.append(str(attr.id))
            filter_fields_sql = "WHERE A.attr_id in ({0})".format(",".join(_fields))

        ci_ids = ",".join(map(str, ci_ids))
        if value_tables is None:
            value_tables = ValueTypeMap.table_name.values()

        value_sql = " UNION ".join([QUERY_CIS_BY_VALUE_TABLE.format(value_table, ci_ids)
                                    for value_table in value_tables])
        query_sql = QUERY_CIS_BY_IDS.format(filter_fields_sql, value_sql)
        # current_app.logger.debug(query_sql)
        cis = db.session.execute(query_sql).fetchall()
        ci_set = set()
        res = list()
        ci_dict = dict()
        unique_id2obj = dict()
        excludes = excludes and set(excludes)
        for ci_id, type_id, attr_id, attr_name, attr_alias, value, value_type, is_list in cis:
            if not fields and excludes and (attr_name in excludes or attr_alias in excludes):
                continue

            if ci_id not in ci_set:
                ci_dict = dict()
                ci_type = CITypeCache.get(type_id)
                ci_dict["_id"] = ci_id
                ci_dict["_type"] = type_id
                ci_dict["ci_type"] = ci_type.name
                ci_dict["ci_type_alias"] = ci_type.alias
                if ci_type.unique_id not in unique_id2obj:
                    unique_id2obj[ci_type.unique_id] = AttributeCache.get(ci_type.unique_id)
                ci_dict["unique"] = unique_id2obj[ci_type.unique_id] and unique_id2obj[ci_type.unique_id].name
                ci_dict["unique_alias"] = unique_id2obj[ci_type.unique_id] and unique_id2obj[ci_type.unique_id].alias
                ci_set.add(ci_id)
                res.append(ci_dict)

            if ret_key == RetKey.NAME:
                attr_key = attr_name
            elif ret_key == RetKey.ALIAS:
                attr_key = attr_alias
            elif ret_key == RetKey.ID:
                attr_key = attr_id
            else:
                return abort(400, ErrFormat.argument_invalid.format("ret_key"))

            value = ValueTypeMap.serialize2[value_type](value)
            if is_list:
                ci_dict.setdefault(attr_key, []).append(value)
            else:
                ci_dict[attr_key] = value

        return res

    @classmethod
    def get_cis_by_ids(cls, ci_ids, ret_key=RetKey.NAME,
                       fields=None, value_tables=None, unique_required=False, excludes=None):
        """

        :param ci_ids: list of CI instance ID, eg. ['1', '2']
        :param ret_key: name, id or alias
        :param fields:
        :param value_tables:
        :param unique_required:
        :param excludes: exclude field list
        :return:
        """

        if not ci_ids:
            return []

        fields = [] if fields is None or not isinstance(fields, list) else fields

        ci_id_tuple = tuple(map(int, ci_ids))
        res = cls._get_cis_from_cache(ci_id_tuple, ret_key, fields, unique_required, excludes=excludes)
        if res is not None:
            return res

        current_app.logger.warning("cache not hit...............")
        return cls._get_cis_from_db(ci_ids, ret_key, fields, value_tables, excludes=excludes)

    @classmethod
    def get_soft_delete_ids(cls):
        return [ci.get("id") for ci in CI.get_by(deleted=True)]


class CIRelationManager(object):
    """
    Manage relation between CIs
    """

    def __init__(self):
        pass

    @classmethod
    def get_children(cls, ci_id, ret_key=RetKey.NAME):
        second_cis = CIRelation.get_by(first_ci_id=ci_id, to_dict=False)
        second_ci_ids = (second_ci.second_ci_id for second_ci in second_cis)
        ci_type2ci_ids = dict()
        for ci_id in second_ci_ids:
            type_id = CI.get_by_id(ci_id).type_id
            ci_type2ci_ids.setdefault(type_id, []).append(ci_id)

        res = {}
        for type_id in ci_type2ci_ids:
            ci_type = CITypeCache.get(type_id)
            children = CIManager.get_cis_by_ids(list(map(str, ci_type2ci_ids[type_id])), ret_key=ret_key)
            res[ci_type.name] = children
        return res

    @staticmethod
    def get_second_cis(first_ci_id, relation_type_id=None, page=1, per_page=None):
        second_cis = db.session.query(CI.id).filter(CI.deleted.is_(False)).join(
            CIRelation, CIRelation.second_ci_id == CI.id).filter(
            CIRelation.first_ci_id == first_ci_id).filter(CIRelation.deleted.is_(False))

        if relation_type_id is not None:
            second_cis = second_cis.filter(CIRelation.relation_type_id == relation_type_id)

        numfound = second_cis.count()
        if per_page != "all":
            second_cis = second_cis.offset((page - 1) * per_page).limit(per_page).all()
        ci_ids = [str(son.id) for son in second_cis]
        result = CIManager.get_cis_by_ids(ci_ids)

        return numfound, len(ci_ids), result

    @staticmethod
    def _sort_handler(sort_by, query_sql):

        if sort_by.startswith("+"):
            sort_type = "asc"
            sort_by = sort_by[1:]
        elif sort_by.startswith("-"):
            sort_type = "desc"
            sort_by = sort_by[1:]
        else:
            sort_type = "asc"
        attr = AttributeCache.get(sort_by)
        if attr is None:
            return query_sql

        attr_id = attr.id
        value_table = TableMap(attr_name=sort_by).table

        ci_table = query_sql.subquery()
        query_sql = db.session.query(ci_table.c.id, value_table.value).join(
            value_table, value_table.ci_id == ci_table.c.id).filter(
            value_table.attr_id == attr_id).filter(ci_table.deleted.is_(False)).order_by(
            getattr(value_table.value, sort_type)())

        return query_sql

    @classmethod
    def get_first_cis(cls, second_ci, relation_type_id=None, page=1, per_page=None):
        first_cis = db.session.query(CIRelation.first_ci_id).filter(
            CIRelation.second_ci_id == second_ci).filter(CIRelation.deleted.is_(False))
        if relation_type_id is not None:
            first_cis = first_cis.filter(CIRelation.relation_type_id == relation_type_id)

        numfound = first_cis.count()
        if per_page != "all":
            first_cis = first_cis.offset((page - 1) * per_page).limit(per_page).all()

        first_ci_ids = [str(first_ci.first_ci_id) for first_ci in first_cis]
        result = CIManager.get_cis_by_ids(first_ci_ids)

        return numfound, len(first_ci_ids), result

    @classmethod
    def get_ancestor_ids(cls, ci_ids, level=1):
        for _ in range(level):
            cis = db.session.query(CIRelation.first_ci_id).filter(
                CIRelation.second_ci_id.in_(ci_ids)).filter(CIRelation.deleted.is_(False))
            ci_ids = [i.first_ci_id for i in cis]

        return ci_ids

    @staticmethod
    def _check_constraint(first_ci_id, second_ci_id, type_relation):
        if type_relation.constraint == ConstraintEnum.Many2Many:
            return

        first_existed = CIRelation.get_by(first_ci_id=first_ci_id, relation_type_id=type_relation.relation_type_id)
        second_existed = CIRelation.get_by(second_ci_id=second_ci_id, relation_type_id=type_relation.relation_type_id)
        if type_relation.constraint == ConstraintEnum.One2One and (first_existed or second_existed):
            return abort(400, ErrFormat.relation_constraint.format("1-1"))

        if type_relation.constraint == ConstraintEnum.One2Many and second_existed:
            return abort(400, ErrFormat.relation_constraint.format("1-N"))

    @classmethod
    def add(cls, first_ci_id, second_ci_id, more=None, relation_type_id=None):

        first_ci = CIManager.confirm_ci_existed(first_ci_id)
        second_ci = CIManager.confirm_ci_existed(second_ci_id)

        existed = CIRelation.get_by(first_ci_id=first_ci_id,
                                    second_ci_id=second_ci_id,
                                    to_dict=False,
                                    first=True)
        if existed is not None:
            if existed.relation_type_id != relation_type_id and relation_type_id is not None:
                existed.update(relation_type_id=relation_type_id)

                CIRelationHistoryManager().add(existed, OperateType.UPDATE)
        else:
            if relation_type_id is None:
                type_relation = CITypeRelation.get_by(parent_id=first_ci.type_id,
                                                      child_id=second_ci.type_id,
                                                      first=True,
                                                      to_dict=False)
                relation_type_id = type_relation and type_relation.relation_type_id
                relation_type_id or abort(404, ErrFormat.relation_not_found.format("{} -> {}".format(
                    first_ci.ci_type.name, second_ci.ci_type.name)))

                if current_app.config.get('USE_ACL'):
                    resource_name = CITypeRelationManager.acl_resource_name(first_ci.ci_type.name,
                                                                            second_ci.ci_type.name)
                    if not ACLManager().has_permission(
                            resource_name,
                            ResourceTypeEnum.CI_TYPE_RELATION,
                            PermEnum.ADD):
                        return abort(403, ErrFormat.no_permission.format(resource_name, PermEnum.ADD))

            else:
                type_relation = CITypeRelation.get_by_id(relation_type_id)

            cls._check_constraint(first_ci_id, second_ci_id, type_relation)

            existed = CIRelation.create(first_ci_id=first_ci_id,
                                        second_ci_id=second_ci_id,
                                        relation_type_id=relation_type_id)

            CIRelationHistoryManager().add(existed, OperateType.ADD)

            ci_relation_cache.apply_async(args=(first_ci_id, second_ci_id), queue=CMDB_QUEUE)

        if more is not None:
            existed.upadte(more=more)

        return existed.id

    @staticmethod
    def delete(cr_id):
        cr = CIRelation.get_by_id(cr_id) or abort(404, ErrFormat.relation_not_found.format("id={}".format(cr_id)))

        if current_app.config.get('USE_ACL'):
            resource_name = CITypeRelationManager.acl_resource_name(cr.first_ci.ci_type.name, cr.second_ci.ci_type.name)
            if not ACLManager().has_permission(
                    resource_name,
                    ResourceTypeEnum.CI_TYPE_RELATION,
                    PermEnum.DELETE):
                return abort(403, ErrFormat.no_permission.format(resource_name, PermEnum.DELETE))

        cr.delete()

        his_manager = CIRelationHistoryManager()
        his_manager.add(cr, operate_type=OperateType.DELETE)

        ci_relation_delete.apply_async(args=(cr.first_ci_id, cr.second_ci_id), queue=CMDB_QUEUE)

        return cr_id

    @classmethod
    def delete_2(cls, first_ci_id, second_ci_id):
        cr = CIRelation.get_by(first_ci_id=first_ci_id,
                               second_ci_id=second_ci_id,
                               to_dict=False,
                               first=True)

        ci_relation_delete.apply_async(args=(first_ci_id, second_ci_id), queue=CMDB_QUEUE)

        return cls.delete(cr.id)

    @classmethod
    def batch_update(cls, ci_ids, parents, children):
        """
        only for many to one
        :param ci_ids:
        :param parents:
        :param children:
        :return:
        """
        if parents is not None and isinstance(parents, list):
            for parent_id in parents:
                for ci_id in ci_ids:
                    cls.add(parent_id, ci_id)

        if children is not None and isinstance(children, list):
            for child_id in children:
                for ci_id in ci_ids:
                    cls.add(ci_id, child_id)

    @classmethod
    def batch_delete(cls, ci_ids, parents):
        """
        only for many to one
        :param ci_ids:
        :param parents:
        :return:
        """

        if parents is not None and isinstance(parents, list):
            for parent_id in parents:
                for ci_id in ci_ids:
                    cls.delete_2(parent_id, ci_id)
