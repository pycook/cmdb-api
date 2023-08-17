# -*- coding:utf-8 -*- 


from api.lib.utils import BaseEnum


class ValueTypeEnum(BaseEnum):
    INT = "0"
    FLOAT = "1"
    TEXT = "2"
    DATETIME = "3"
    DATE = "4"
    TIME = "5"
    JSON = "6"


class ConstraintEnum(BaseEnum):
    One2Many = "0"
    One2One = "1"
    Many2Many = "2"


class CIStatusEnum(BaseEnum):
    REVIEW = "0"
    VALIDATE = "1"


class ExistPolicy(BaseEnum):
    REJECT = "reject"
    NEED = "need"
    IGNORE = "ignore"
    REPLACE = "replace"


class OperateType(BaseEnum):
    ADD = "0"
    DELETE = "1"
    UPDATE = "2"
    SOFT_DELETE = "3"


class CITypeOperateType(BaseEnum):
    ADD = "0"  # 新增模型
    UPDATE = "1"  # 修改模型
    DELETE = "2"  # 删除模型
    ADD_ATTRIBUTE = "3"  # 新增属性
    UPDATE_ATTRIBUTE = "4"  # 修改属性
    DELETE_ATTRIBUTE = "5"  # 删除属性
    ADD_TRIGGER = "6"  # 新增触发器
    UPDATE_TRIGGER = "7"  # 修改触发器
    DELETE_TRIGGER = "8"  # 删除触发器
    ADD_UNIQUE_CONSTRAINT = "9"  # 新增联合唯一
    UPDATE_UNIQUE_CONSTRAINT = "10"  # 修改联合唯一
    DELETE_UNIQUE_CONSTRAINT = "11"  # 删除联合唯一
    ADD_RELATION = "12"  # 新增关系
    DELETE_RELATION = "13"  # 删除关系


class RetKey(BaseEnum):
    ID = "id"
    NAME = "name"
    ALIAS = "alias"


class ResourceTypeEnum(BaseEnum):
    CI = "CIType"
    CI_TYPE = "CIType"  # create/update/delete/read/config/grant
    CI_TYPE_RELATION = "CITypeRelation"  # create/delete/grant
    RELATION_VIEW = "RelationView"  # read/update/delete/grant
    CI_FILTER = "CIFilter"  # read


class PermEnum(BaseEnum):
    ADD = "create"
    UPDATE = "update"
    DELETE = "delete"
    READ = "read"
    CONFIG = "config"
    GRANT = "grant"


class RoleEnum(BaseEnum):
    CONFIG = "cmdb_admin"
    CMDB_READ_ALL = "CMDB_READ_ALL"


class AutoDiscoveryType(BaseEnum):
    AGENT = "agent"
    SNMP = "snmp"
    HTTP = "http"


class AttributeDefaultValueEnum(BaseEnum):
    CREATED_AT = "$created_at"
    UPDATED_AT = "$updated_at"
    AUTO_INC_ID = "$auto_inc_id"


CMDB_QUEUE = "one_cmdb_async"
REDIS_PREFIX_CI = "ONE_CMDB"
REDIS_PREFIX_CI_RELATION = "CMDB_CI_RELATION"

L_TYPE = None
L_CI = None
