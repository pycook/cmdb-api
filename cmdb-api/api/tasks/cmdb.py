# -*- coding:utf-8 -*- 


import json
import time

import jinja2
import requests
from flask import current_app

import api.lib.cmdb.ci
from api.extensions import celery
from api.extensions import db
from api.extensions import es
from api.extensions import rd
from api.lib.cmdb.cache import CITypeAttributesCache
from api.lib.cmdb.const import CMDB_QUEUE
from api.lib.cmdb.const import REDIS_PREFIX_CI
from api.lib.cmdb.const import REDIS_PREFIX_CI_RELATION
from api.lib.mail import send_mail
from api.lib.utils import Lock
from api.models.cmdb import CIRelation


@celery.task(name="cmdb.ci_cache", queue=CMDB_QUEUE)
def ci_cache(ci_id):
    time.sleep(0.01)
    db.session.remove()

    m = api.lib.cmdb.ci.CIManager()
    ci_dict = m.get_ci_by_id_from_db(ci_id, need_children=False, use_master=False)

    if current_app.config.get("USE_ES"):
        es.create_or_update(ci_id, ci_dict)
    else:
        rd.create_or_update({ci_id: json.dumps(ci_dict)}, REDIS_PREFIX_CI)

    current_app.logger.info("{0} flush..........".format(ci_id))


@celery.task(name="cmdb.batch_ci_cache", queue=CMDB_QUEUE)
def batch_ci_cache(ci_ids):
    time.sleep(1)
    db.session.remove()

    for ci_id in ci_ids:
        m = api.lib.cmdb.ci.CIManager()
        ci_dict = m.get_ci_by_id_from_db(ci_id, need_children=False, use_master=False)

        if current_app.config.get("USE_ES"):
            es.create_or_update(ci_id, ci_dict)
        else:
            rd.create_or_update({ci_id: json.dumps(ci_dict)}, REDIS_PREFIX_CI)

        current_app.logger.info("{0} flush..........".format(ci_id))


@celery.task(name="cmdb.ci_delete", queue=CMDB_QUEUE)
def ci_delete(ci_id):
    current_app.logger.info(ci_id)

    if current_app.config.get("USE_ES"):
        es.delete(ci_id)
    else:
        rd.delete(ci_id, REDIS_PREFIX_CI)

    current_app.logger.info("{0} delete..........".format(ci_id))


@celery.task(name="cmdb.ci_relation_cache", queue=CMDB_QUEUE)
def ci_relation_cache(parent_id, child_id):
    db.session.remove()

    with Lock("CIRelation_{}".format(parent_id)):
        children = rd.get([parent_id], REDIS_PREFIX_CI_RELATION)[0]
        children = json.loads(children) if children is not None else {}

        cr = CIRelation.get_by(first_ci_id=parent_id, second_ci_id=child_id, first=True, to_dict=False)
        if str(child_id) not in children:
            children[str(child_id)] = cr.second_ci.type_id

        rd.create_or_update({parent_id: json.dumps(children)}, REDIS_PREFIX_CI_RELATION)

    current_app.logger.info("ADD ci relation cache: {0} -> {1}".format(parent_id, child_id))


@celery.task(name="cmdb.ci_relation_delete", queue=CMDB_QUEUE)
def ci_relation_delete(parent_id, child_id):
    with Lock("CIRelation_{}".format(parent_id)):
        children = rd.get([parent_id], REDIS_PREFIX_CI_RELATION)[0]
        children = json.loads(children) if children is not None else {}

        if str(child_id) in children:
            children.pop(str(child_id))

        rd.create_or_update({parent_id: json.dumps(children)}, REDIS_PREFIX_CI_RELATION)

    current_app.logger.info("DELETE ci relation cache: {0} -> {1}".format(parent_id, child_id))


@celery.task(name="cmdb.ci_type_attribute_order_rebuild", queue=CMDB_QUEUE)
def ci_type_attribute_order_rebuild(type_id):
    current_app.logger.info('rebuild attribute order')
    db.session.remove()

    from api.lib.cmdb.ci_type import CITypeAttributeGroupManager

    attrs = CITypeAttributesCache.get(type_id)
    id2attr = {attr.attr_id: attr for attr in attrs}

    res = CITypeAttributeGroupManager.get_by_type_id(type_id, True)
    order = 0
    for group in res:
        for _attr in group.get('attributes'):
            if order != id2attr.get(_attr['id']) and id2attr.get(_attr['id']):
                id2attr.get(_attr['id']).update(order=order)

            order += 1


@celery.task(name='cmdb.trigger_notify', queue=CMDB_QUEUE)
def trigger_notify(notify, ci_id):
    from api.lib.perm.acl.cache import UserCache

    def _wrap_mail(mail_to):
        if "@" not in mail_to:
            user = UserCache.get(mail_to)
            if user:
                return user.email

        return mail_to

    db.session.remove()

    m = api.lib.cmdb.ci.CIManager()
    ci_dict = m.get_ci_by_id_from_db(ci_id, need_children=False, use_master=False)

    subject = jinja2.Template(notify.get('subject') or "").render(ci_dict)
    body = jinja2.Template(notify.get('body') or "").render(ci_dict)

    if notify.get('wx_to'):
        to_user = jinja2.Template('|'.join(notify['wx_to'])).render(ci_dict)
        url = current_app.config.get("WX_URI")
        data = {"to_user": to_user, "content": subject}
        try:
            requests.post(url, data=data)
        except Exception as e:
            current_app.logger.error(str(e))

    if notify.get('mail_to'):
        try:
            if len(subject) > 700:
                subject = subject[:600] + "..." + subject[-100:]

            send_mail("", [_wrap_mail(jinja2.Template(i).render(ci_dict))
                           for i in notify['mail_to'] if i], subject, body)
        except Exception as e:
            current_app.logger.error("Send mail failed: {0}".format(str(e)))


@celery.task(name='cmdb.delete_soft_deleted_ci', queue=CMDB_QUEUE)
def delete_soft_deleted_ci(ci_id):
    current_app.logger.info("delete_soft_deleted_ci: {}".format(ci_id))

    from api.app import create_app
    from flask_login import login_user
    from api.lib.perm.acl.cache import UserCache

    app = create_app()
    app.test_request_context().push()
    login_user(UserCache.get('worker'))

    manager = api.lib.cmdb.ci.CIManager()
    manager.delete(ci_id)
