# -*- coding: utf-8 -*-

import redis
import boto3
import os
import json

from contextlib import contextmanager

from sqlalchemy import engine_from_config, MetaData, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import func

__all__ = ['ModelBase', 'db_session_manager']


class _DbManager(object):
    def __init__(self):
        self.__session_maker_dict = {}
        self.__engine_dict = {}
        self.__mate_dict = {}
        self.__scoped_session_factory_dict = {}

    @staticmethod
    def __connect_handle(dbapi_connection, connection_record):
        dbapi_connection.query('SET time_zone=\'+08:00\';')

    def __set_engine(self, db_config, name):
        engine = engine_from_config(db_config, '', encoding="utf-8")
        event.listen(engine, 'connect', self.__connect_handle)
        self.__engine_dict[name] = engine

    def __get_engine(self, name):
        return self.__engine_dict[name]

    def __create_session_maker(self, name):
        engine = self.__get_engine(name)
        return sessionmaker(bind=engine)

    def __create_meta(self, name):
        engine = self.__get_engine(name)
        return MetaData(bind=engine)

    def __create_scoped_session_factory(self, name):
        session_maker = self.__session_maker_dict[name]
        return scoped_session(session_maker)

    def register_db(self, db_config, name='default'):
        self.__set_engine(db_config, name)
        self.__session_maker_dict[name] = self.__create_session_maker(name)
        self.__mate_dict[name] = self.__create_meta(name)
        self.__scoped_session_factory_dict[name] = self.__create_scoped_session_factory(name)

    @contextmanager
    def with_session(self, name='default'):
        session_maker = self.__session_maker_dict[name]
        session = session_maker()
        try:
            session.expire_on_commit = False
            yield session
        finally:
            session.close()

    @contextmanager
    def with_connection(self, name='default'):
        engine = self.__get_engine(name)
        connection = engine.connect()
        try:
            yield connection
        finally:
            connection.close()

    def get_engine(self, name='default'):
        engine = self.__get_engine(name)
        return engine

    def get_session(self, name='default'):
        session_maker = self.__session_maker_dict[name]
        return session_maker()

    def get_scoped_session(self, name='default'):
        return self.__scoped_session_factory_dict[name]

    def get_meta_data(self, name='default'):
        return self.__mate_dict[name]


db_session_manager = _DbManager()

ModelBase = declarative_base()


class _RedisManager(object):
    def __init__(self):
        self.__pool = {}

    def register_db(self, db_config, name='default'):
        if name in self.__pool:
            return True
        self.__pool[name] = redis.ConnectionPool(**db_config)

    def get_client(self, name='default'):
        pool = self.__pool[name]
        return redis.Redis(connection_pool=pool)

    @contextmanager
    def with_pipeline(self, name='default'):
        pool = self.__pool[name]
        r = redis.Redis(connection_pool=pool)
        p = r.pipeline()
        try:
            yield p
        finally:
            p.execute()

redis_manager = _RedisManager()

db_server_now = func.now
