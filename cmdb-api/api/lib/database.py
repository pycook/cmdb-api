# -*- coding:utf-8 -*-

import datetime

import six

from api.extensions import db
from api.lib.exception import CommitException


class FormatMixin(object):
    def to_dict(self):
        res = dict([(k, getattr(self, k) if not isinstance(
            getattr(self, k), (datetime.datetime, datetime.date, datetime.time)) else str(
            getattr(self, k))) for k in getattr(self, "__mapper__").c.keys()])
        # FIXME: getattr(cls, "__table__").columns  k.name

        res.pop('password', None)
        res.pop('_password', None)
        res.pop('secret', None)

        return res

    @classmethod
    def from_dict(cls, **kwargs):
        from sqlalchemy.sql.sqltypes import Time, Date, DateTime

        columns = dict(getattr(cls, "__table__").columns)

        for k, c in columns.items():
            if kwargs.get(k):
                if type(c.type) == Time:
                    kwargs[k] = datetime.datetime.strptime(kwargs[k], "%H:%M:%S").time()
                if type(c.type) == Date:
                    kwargs[k] = datetime.datetime.strptime(kwargs[k], "%Y-%m-%d").date()
                if type(c.type) == DateTime:
                    kwargs[k] = datetime.datetime.strptime(kwargs[k], "%Y-%m-%d %H:%M:%S")

        return cls(**kwargs)

    @classmethod
    def get_columns(cls):
        return {k: 1 for k in getattr(cls, "__mapper__").c.keys()}


class CRUDMixin(FormatMixin):
    @classmethod
    def create(cls, flush=False, commit=True, **kwargs):
        return cls(**kwargs).save(flush=flush, commit=commit)

    def update(self, flush=False, commit=True, filter_none=True, **kwargs):
        kwargs.pop("id", None)
        for attr, value in six.iteritems(kwargs):
            if (value is not None and filter_none) or not filter_none:
                setattr(self, attr, value)

        return self.save(flush=flush, commit=commit)

    def save(self, commit=True, flush=False):
        db.session.add(self)
        try:
            if flush:
                db.session.flush()
            elif commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CommitException(str(e))

        return self

    def delete(self, flush=False, commit=True):
        db.session.delete(self)
        try:
            if flush:
                return db.session.flush()
            elif commit:
                return db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CommitException(str(e))

    def soft_delete(self, flush=False, commit=True):
        setattr(self, "deleted", True)
        setattr(self, "deleted_at", datetime.datetime.now())
        self.save(flush=flush, commit=commit)

    @classmethod
    def get_by_id(cls, _id, with_soft_deleted=False):
        if any((isinstance(_id, six.string_types) and _id.isdigit(),
                isinstance(_id, (six.integer_types, float))), ):
            obj = getattr(cls, "query").get(int(_id))
            if obj and (with_soft_deleted or not obj.deleted):
                return obj

    @classmethod
    def get_by(cls, first=False,
               to_dict=True,
               fl=None,
               exclude=None,
               deleted=False,
               use_master=False,
               only_query=False,
               **kwargs):
        db_session = db.session if not use_master else db.session().using_bind("master")
        fl = fl.strip().split(",") if fl and isinstance(fl, six.string_types) else (fl or [])
        exclude = exclude.strip().split(",") if exclude and isinstance(exclude, six.string_types) else (exclude or [])

        keys = cls.get_columns()
        fl = [k for k in fl if k in keys]
        fl = [k for k in keys if k not in exclude and not k.isupper()] if exclude else fl
        fl = list(filter(lambda x: "." not in x, fl))

        if hasattr(cls, "deleted") and deleted is not None:
            kwargs["deleted"] = deleted

        kwargs_for_func = {i[7:]: kwargs[i] for i in kwargs if i.startswith('__func_')}
        kwargs = {i: kwargs[i] for i in kwargs if not i.startswith('__func_')}

        if fl:
            query = db_session.query(*[getattr(cls, k) for k in fl])
        else:
            query = db_session.query(cls)

        query = query.filter_by(**kwargs)
        for i in kwargs_for_func:
            func, key = i.split('__key_')
            query = query.filter(getattr(getattr(cls, key), func)(kwargs_for_func[i]))

        if only_query:
            return query

        if fl:
            result = [{k: getattr(i, k) for k in fl} if to_dict else i for i in query]
        else:
            result = [i.to_dict() if to_dict else i for i in query]

        return result[0] if first and result else (None if first else result)

    @classmethod
    def get_by_like(cls, to_dict=True, deleted=False, **kwargs):
        query = db.session.query(cls)
        if hasattr(cls, "deleted") and deleted is not None:
            query = query.filter(cls.deleted.is_(deleted))

        for k, v in kwargs.items():
            query = query.filter(getattr(cls, k).ilike('%{0}%'.format(v)))
        return [i.to_dict() if to_dict else i for i in query]


class SoftDeleteMixin(object):
    deleted_at = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, index=True, default=False)


class TimestampMixin(object):
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=lambda: datetime.datetime.now())


class TimestampMixin2(object):
    created_at = db.Column(db.DateTime, default=lambda: datetime.datetime.now(), index=True)


class SurrogatePK(object):
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Model(SoftDeleteMixin, TimestampMixin, CRUDMixin, db.Model, SurrogatePK):
    __abstract__ = True


class CRUDModel(db.Model, CRUDMixin):
    __abstract__ = True


class Model2(TimestampMixin2, db.Model, CRUDMixin, SurrogatePK):
    __abstract__ = True
