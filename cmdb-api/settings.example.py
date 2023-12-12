# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SECRET_KEY = env.str("SECRET_KEY")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
DEBUG_TB_ENABLED = DEBUG
DEBUG_TB_INTERCEPT_REDIRECTS = False

ERROR_CODES = [400, 401, 403, 404, 405, 500, 502]

# # database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{db}?charset=utf8'
SQLALCHEMY_BINDS = {
    "user": 'mysql+pymysql://{user}:{password}@127.0.0.1:3306/{db}?charset=utf8'
}
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_recycle': 300,
}

# # cache
CACHE_TYPE = "redis"
CACHE_REDIS_HOST = "127.0.0.1"
CACHE_REDIS_PORT = 6379
CACHE_REDIS_PASSWORD = ""
CACHE_KEY_PREFIX = "CMDB::"
CACHE_DEFAULT_TIMEOUT = 3000

# # log
LOG_PATH = './logs/app.log'
LOG_LEVEL = 'DEBUG'

# # mail
MAIL_SERVER = ''
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
DEFAULT_MAIL_SENDER = ''

# # queue
CELERY = {
    "broker_url": 'redis://127.0.0.1:6379/2',
    "result_backend": "redis://127.0.0.1:6379/2",
    "broker_vhost": "/",
    "broker_connection_retry_on_startup": True
}
ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': CELERY['broker_url'],
    }
}

# =============================== Authentication ===========================================================

# # CAS
AUTH_WITH_CAS = False
CAS_SERVER = "https://{your-casdoor-hostname}"
CAS_VALIDATE_SERVER = "https://{your-casdoor-hostname}"
CAS_LOGIN_ROUTE = "/cas/built-in/cas/login"
CAS_LOGOUT_ROUTE = "/cas/built-in/cas/logout"
CAS_VALIDATE_ROUTE = "/cas/built-in/cas/serviceValidate"
CAS_AFTER_LOGIN = "/"
CAS_USER_MAP = {
    "username": {"tag": "cas:user"},
    "nickname": {"tag": "cas:attribute", "attrs": {"name": "displayName"}},
    "email": {"tag": "cas:attribute", "attrs": {"name": "email"}},
    "mobile": {"tag": "cas:attribute", "attrs": {"name": "phone"}},
    "avatar": {"tag": "cas:attribute", "attrs": {"name": "avatar"}},
}

# # OAuth2.0
AUTH_WITH_OAUTH2 = False
OAUTH2_CLIENT_ID = ""
OAUTH2_CLIENT_SECRET = ""
OAUTH2_AUTHORIZE_URL = "https://{your-casdoor-hostname}/login/oauth/authorize"
OAUTH2_TOKEN_URL = "https://{your-casdoor-hostname}/api/login/oauth/access_token"
OAUTH2_USER_INFO = {
    "url": "https://{your-casdoor-hostname}/api/userinfo",
    "email": lambda x: x['email'],
    "username": lambda x: x['name']
}
OAUTH2_SCOPES = ["profile email"]
OAUTH2_AFTER_LOGIN = "/"

# # OIDC
AUTH_WITH_OIDC = False
OIDC_CLIENT_ID = ""
OIDC_CLIENT_SECRET = ""
OIDC_AUTHORIZE_URL = "https://{your-casdoor-hostname}/login/oauth/authorize"
OIDC_TOKEN_URL = "https://{your-casdoor-hostname}/api/login/oauth/access_token"
OIDC_USER_INFO = {
    "url": "https://{your-casdoor-hostname}/api/userinfo",
    "email": lambda x: x['email'],
    "username": lambda x: x['name']
}
OIDC_SCOPES = ["openid profile email"]
OIDC_AFTER_LOGIN = "/"

# # LDAP
AUTH_WITH_LDAP = False
LDAP_SERVER = ''
LDAP_DOMAIN = ''
LDAP_USER_DN = 'cn={},ou=users,dc=xxx,dc=com'
# ==========================================================================================================

# # pagination
DEFAULT_PAGE_COUNT = 50

# # permission
WHITE_LIST = ["127.0.0.1"]
USE_ACL = True

# # elastic search
ES_HOST = '127.0.0.1'
USE_ES = False

BOOL_TRUE = ['true', 'TRUE', 'True', True, '1', 1, "Yes", "YES", "yes", 'Y', 'y']

# # messenger
USE_MESSENGER = True

# # secrets
SECRETS_ENGINE = 'inner'  # 'inner' or 'vault'
VAULT_URL = ''
VAULT_TOKEN = ''
INNER_TRIGGER_TOKEN = ''
