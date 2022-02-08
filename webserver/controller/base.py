#!/usr/bin/env python3
# Time: 2017/10/16 15:24

__author__ = 'wgs@test'


import traceback
import logging
# import climate
# logging = climate.get_logger(__name__)

from functools import wraps
from flask.views import MethodView
from flask import request, jsonify

from apis.sql_manage_api import SqlManageApi


class Base(MethodView):
    def __init__(self, db_session=None):
        self.__sql_manage_api = SqlManageApi()

    @classmethod
    def set_response(cls, **kwargs):
        response = {
            "status": True,
            "error_code": 0,
            "message": "",
            "result": {}
        }
        response.update(kwargs)
        # logging.info('>>>>> [Return] json： %s' % response)
        return jsonify(response)


    @classmethod
    def check_exception(cls, func):
        @wraps(func)
        def wrapse(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.info(traceback.format_exc())
                # logging.error(traceback.format_exc())
                return cls.set_response(status=False, error_code=-1, message=str(e))
        return wrapse

    def exec_sql(self, sql_type, sql):
        logging.info("sql: %s" % sql)
        if sql_type == 'select':
            status, result = self.__sql_manage_api.select_info(sql)
            info = [dict(row) for row in result]

        else:
            status, result = self.__sql_manage_api.other_info(sql)
            info = result.rowcount

        print("sql result: ", status, info)

        return status, info