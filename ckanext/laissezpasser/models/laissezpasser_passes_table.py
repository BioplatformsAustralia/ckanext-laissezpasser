# encoding: utf-8

import datetime
from sqlalchemy import Column, Table, ForeignKey, orm
from sqlalchemy import types as _types
from ckan.model import meta, Package, User, domain_object


__all__ = [u"LaissezpasserPassesTable", u"laissezpasser_passes_table"]

laissezpasser_passes_table = Table(
    u"laissezpasser_passes",
    meta.metadata,
    Column(u"dataset", _types.UnicodeText, ForeignKey('package.name'), primary_key=True, nullable=False),        
    Column(u"user_name", _types.UnicodeText, ForeignKey('user.name'), primary_key=True, nullable=False),
    Column(u"created_at", _types.DateTime, default=datetime.datetime.utcnow, nullable=False),
    Column(u"created_by", _types.UnicodeText, nullable=False),
    Column(u"valid_until", _types.DateTime(timezone=False), nullable=False)
)


class LaissezpasserPassesTable(domain_object.DomainObject):
    def __init__(self, dataset_name=None, user=None, created_at=None, created_by=None, valid_until=None):
        self.dataset = dataset_name
        self.user = user        
        self.created_at = created_at
        self.created_by = created_by
        self.valid_until = valid_until

    
    @classmethod
    def get_by_package(cls, name, autoflush=True):
        if not name:
            return None

        exists = meta.Session.query(cls).filter(cls.dataset==name).first() is not None
        if not exists:
            return False
        query = meta.Session.query(cls).filter(cls.dataset==name)
        query = query.autoflush(autoflush)
        record = query.all()
        return record


    @classmethod
    def get_by_user(cls, name, autoflush=True):
        if not name:
            return None

        exists = meta.Session.query(cls).filter(cls.user_name==name).first() is not None
        if not exists:
            return False
        query = meta.Session.query(cls).filter(cls.user_name==name)
        query = query.autoflush(autoflush)
        record = query.all()
        return record


    @classmethod
    def get_by_package_and_user(cls, dataset, user, autoflush=True):
        if not dataset and not user:
            return None

        exists = meta.Session.query(cls).filter(cls.dataset==dataset, cls.user_name==user).first() is not None
        if not exists:
            return False
        query = meta.Session.query(cls).filter(cls.dataset==dataset, cls.user_name==user)
        query = query.autoflush(autoflush)
        record = query.all()
        return record



meta.mapper(
    LaissezpasserPassesTable,
    laissezpasser_passes_table,
    properties={
        u"package": orm.relation(
            Package, backref=orm.backref(u"laissezpasser_passes_table", cascade=u"all, delete, delete-orphan")
        ),
        u"user": orm.relation(
            User, backref=orm.backref(u"laissezpasser_passes_table", cascade=u"all, delete, delete-orphan")
        ),
    },
)
