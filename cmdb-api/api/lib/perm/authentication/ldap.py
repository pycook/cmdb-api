# -*- coding:utf-8 -*-

import uuid

from flask import current_app
from flask import session
from ldap3 import ALL
from ldap3 import AUTO_BIND_NO_TLS
from ldap3 import Connection
from ldap3 import Server
from ldap3.core.exceptions import LDAPBindError
from ldap3.core.exceptions import LDAPCertificateError

from api.lib.perm.acl.audit import AuditCRUD
from api.lib.perm.acl.resp_format import ErrFormat
from api.models.acl import User


def authenticate_with_ldap(username, password):
    server = Server(current_app.config.get('LDAP').get('ldap_server'), get_info=ALL, connect_timeout=3)
    if '@' in username:
        email = username
        who = current_app.config['LDAP'].get('ldap_user_dn').format(username.split('@')[0])
    else:
        who = current_app.config['LDAP'].get('ldap_user_dn').format(username)
        email = "{}@{}".format(who, current_app.config['LDAP'].get('ldap_domain'))

    username = username.split('@')[0]
    user = User.query.get_by_username(username)
    try:
        if not password:
            raise LDAPCertificateError

        try:
            conn = Connection(server, user=who, password=password, auto_bind=AUTO_BIND_NO_TLS)
        except LDAPBindError:
            conn = Connection(server,
                              user=f"{username}@{current_app.config['LDAP'].get('ldap_domain')}",
                              password=password,
                              auto_bind=AUTO_BIND_NO_TLS)

        if conn.result['result'] != 0:
            AuditCRUD.add_login_log(username, False, ErrFormat.invalid_password)
            raise LDAPBindError
        else:
            _id = AuditCRUD.add_login_log(username, True, ErrFormat.login_succeed)
            session['LOGIN_ID'] = _id

        if not user:
            from api.lib.perm.acl.user import UserCRUD
            user = UserCRUD.add(username=username, email=email, password=uuid.uuid4().hex)

        return user, True
    except LDAPBindError as e:
        current_app.logger.info(e)
        return user, False
