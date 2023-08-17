# -*- coding:utf-8 -*-

import time

import six
from flask import abort
from flask import current_app
from flask import request

from api.lib.cmdb.cache import CITypeCache
from api.lib.cmdb.ci import CIManager
from api.lib.cmdb.ci import CIRelationManager
from api.lib.cmdb.const import ExistPolicy, CMDB_QUEUE
from api.lib.cmdb.const import ResourceTypeEnum, PermEnum
from api.lib.cmdb.const import RetKey
from api.lib.cmdb.perms import has_perm_for_ci
from api.lib.cmdb.search import SearchError
from api.lib.cmdb.search.ci import search
from api.lib.perm.acl.acl import has_perm_from_args
from api.lib.utils import get_page
from api.lib.utils import get_page_size
from api.lib.utils import handle_arg_list
from api.models.cmdb import CI
from api.resource import APIView


class CIsByTypeView(APIView):
    url_prefix = "/ci/type/<int:type_id>"

    def get(self, type_id):
        fields = handle_arg_list(request.values.get("fields", ""))

        ret_key = request.values.get("ret_key", RetKey.NAME)
        if ret_key not in (RetKey.NAME, RetKey.ALIAS, RetKey.ID):
            ret_key = RetKey.NAME

        page = get_page(request.values.get("page", 1))
        count = get_page_size(request.values.get("count"))

        manager = CIManager()
        res = manager.get_cis_by_type(type_id,
                                      ret_key=ret_key,
                                      fields=fields,
                                      page=page,
                                      per_page=count)

        return self.jsonify(type_id=type_id,
                            numfound=res[0],
                            total=len(res[2]),
                            page=res[1],
                            cis=res[2])


class CIView(APIView):
    url_prefix = ("/ci/<int:ci_id>", "/ci")

    def get(self, ci_id):
        fields = handle_arg_list(request.values.get("fields", ""))

        ret_key = request.values.get("ret_key", RetKey.NAME)
        if ret_key not in (RetKey.NAME, RetKey.ALIAS, RetKey.ID):
            ret_key = RetKey.NAME

        manager = CIManager()
        ci = manager.get_ci_by_id_from_db(ci_id, ret_key=ret_key, fields=fields, valid=True)

        return self.jsonify(ci_id=ci_id, ci=ci)

    @staticmethod
    def _wrap_ci_dict():
        ci_dict = {k: v.strip() if isinstance(v, six.string_types) else v for k, v in request.values.items()
                   if k != "ci_type" and not k.startswith("_")}

        return ci_dict

    @has_perm_for_ci("ci_type", ResourceTypeEnum.CI, PermEnum.ADD, lambda x: CITypeCache.get(x))
    def post(self):
        ci_type = request.values.get("ci_type")
        _no_attribute_policy = request.values.get("no_attribute_policy", ExistPolicy.IGNORE)

        exist_policy = request.values.pop('exist_policy', None)

        ci_dict = self._wrap_ci_dict()

        manager = CIManager()
        current_app.logger.debug(ci_dict)
        ci_id = manager.add(ci_type,
                            exist_policy=exist_policy or ExistPolicy.REJECT,
                            _no_attribute_policy=_no_attribute_policy,
                            _is_admin=request.values.pop('__is_admin', False),
                            **ci_dict)

        return self.jsonify(ci_id=ci_id)

    @has_perm_for_ci("ci_id", ResourceTypeEnum.CI, PermEnum.UPDATE, CIManager.get_type)
    def put(self, ci_id=None):
        args = request.values
        current_app.logger.info(args)
        ci_type = args.get("ci_type")
        _no_attribute_policy = args.get("no_attribute_policy", ExistPolicy.IGNORE)

        ci_dict = self._wrap_ci_dict()
        manager = CIManager()
        if ci_id is not None:
            manager.update(ci_id,
                           _is_admin=request.values.pop('__is_admin', False),
                           **ci_dict)
        else:
            ci_id = manager.add(ci_type,
                                exist_policy=ExistPolicy.REPLACE,
                                _no_attribute_policy=_no_attribute_policy,
                                _is_admin=request.values.pop('__is_admin', False),
                                **ci_dict)

        return self.jsonify(ci_id=ci_id)

    @has_perm_for_ci("ci_id", ResourceTypeEnum.CI, PermEnum.DELETE, CIManager.get_type)
    def delete(self, ci_id):
        manager = CIManager()
        manager.delete(ci_id)

        return self.jsonify(message="ok")


class CIDetailView(APIView):
    url_prefix = "/ci/<int:ci_id>/detail"

    def get(self, ci_id):
        _ci = CI.get_by_id(ci_id).to_dict()

        return self.jsonify(**_ci)


class CISearchView(APIView):
    url_prefix = ("/ci/s", "/ci/search")

    def get(self):
        """@params: q: query statement
                    fl: filter by column
                    count/page_size: the number of ci
                    ret_key: id, name, alias
                    facet: statistic
        """
        page = get_page(request.values.get("page", 1))
        count = get_page_size(request.values.get("count") or request.values.get("page_size"))

        query = request.values.get('q', "")
        fl = handle_arg_list(request.values.get('fl', ""))
        excludes = handle_arg_list(request.values.get('excludes', ""))
        ret_key = request.values.get('ret_key', RetKey.NAME)
        if ret_key not in (RetKey.NAME, RetKey.ALIAS, RetKey.ID):
            ret_key = RetKey.NAME
        facet = handle_arg_list(request.values.get("facet", ""))
        sort = request.values.get("sort")

        start = time.time()
        s = search(query, fl, facet, page, ret_key, count, sort, excludes)
        try:
            response, counter, total, page, numfound, facet = s.search()
        except SearchError as e:
            return abort(400, str(e))

        if request.values.get('need_children') in current_app.config.get('BOOL_TRUE') and len(response) == 1:
            children = CIRelationManager.get_children(response[0]['_id'], ret_key=ret_key)  # one floor
            response[0].update(children)

        current_app.logger.debug("search time is: {0}".format(time.time() - start))

        return self.jsonify(numfound=numfound,
                            total=total,
                            page=page,
                            facet=facet,
                            counter=counter,
                            result=response)

    def post(self):
        return self.get()


class CIUnique(APIView):
    url_prefix = "/ci/<int:ci_id>/unique"

    @has_perm_from_args("ci_id", ResourceTypeEnum.CI, PermEnum.UPDATE, CIManager.get_type_name)
    def put(self, ci_id):
        params = request.values
        unique_name = params.keys()[0]
        unique_value = params.values()[0]

        CIManager.update_unique_value(ci_id, unique_name, unique_value)

        return self.jsonify(ci_id=ci_id)


class CIHeartbeatView(APIView):
    url_prefix = ("/ci/heartbeat", "/ci/heartbeat/<string:ci_type>/<string:unique>")

    def get(self):
        page = get_page(request.values.get("page", 1))
        ci_type = request.values.get("ci_type", "").strip()
        try:
            type_id = CITypeCache.get(ci_type).type_id
        except AttributeError:
            return self.jsonify(numfound=0, result=[])
        agent_status = request.values.get("agent_status")
        if agent_status:
            agent_status = int(agent_status)

        numfound, result = CIManager.get_heartbeat(page, type_id, agent_status=agent_status)

        return self.jsonify(numfound=numfound, result=result)

    def post(self, ci_type, unique):
        if not unique or not ci_type:
            return self.jsonify(message="error")

        msg, cmd = CIManager().add_heartbeat(ci_type, unique)

        return self.jsonify(message=msg, cmd=cmd)


class CIFlushView(APIView):
    url_prefix = ("/ci/flush", "/ci/<int:ci_id>/flush")

    # @auth_abandoned
    def get(self, ci_id=None):
        from api.tasks.cmdb import ci_cache
        from api.lib.cmdb.const import CMDB_QUEUE
        if ci_id is not None:
            ci_cache.apply_async([ci_id], queue=CMDB_QUEUE)
        else:
            cis = CI.get_by(to_dict=False)
            for ci in cis:
                ci_cache.apply_async([ci.id], queue=CMDB_QUEUE)

        return self.jsonify(code=200)


class CIAutoDiscoveryStatisticsView(APIView):
    url_prefix = "/ci/adc/statistics"

    def get(self):
        return self.jsonify(CIManager.get_ad_statistics())


class SoftDeleteCis(APIView):
    url_prefix = ("/ci/soft_deleted/cis",)

    def get(self):
        manager = CIManager()
        ids = manager.get_soft_delete_ids()
        return self.jsonify({"count": len(ids), "ids": ids})

    def delete(self):
        from api.tasks.cmdb import delete_soft_deleted_ci
        manager = CIManager()
        ids = manager.get_soft_delete_ids()
        for _id in ids:
            delete_soft_deleted_ci.apply_async([_id], queue=CMDB_QUEUE)
        return self.jsonify(message="add {} ci to celery".format(len(ids)))
