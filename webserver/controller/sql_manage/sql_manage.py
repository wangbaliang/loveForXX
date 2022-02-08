#!/usr/bin/env python3
# Time: 2018/12/12 下午9:48
import hashlib
import time

from apis.sql_manage_api import SqlManageApi
from utils.config_helper import config

__author__ = 'hjj@test'


from flask import request, jsonify

from controller.base import Base

# import climate
# logging = climate.get_logger(__name__)


class SqlManage(Base):
    def __init__(self):
        super(SqlManage, self).__init__()
        self.__sql_manage_api = SqlManageApi()

    def get(self):
        pass

    @Base.check_exception
    def post(self):
        args = request.get_json(force=True)
        sql = args.get('sql', '')
        sql_type = args.get('sql_type', '')
        timestamp = args.get('timestamp', 0)
        auth_key = args.get('auth_key', '')
        system_token = config.get('sql_manager_token')
        now_timestamp = int(time.time())
        # 验证auth_key
        if now_timestamp - int(timestamp) > 120:
            return self.set_response(**{'status': False, 'message': 'auth_key error', 'error_code': -1})
        if not auth_key:
            return self.set_response(**{'status': False, 'message': 'token is null', 'error_code': -1})
        md5_value_str = str(sql) + str(sql_type) + str(timestamp) + str(system_token)
        md5_value = hashlib.md5(md5_value_str.encode(encoding='UTF-8')).hexdigest()
        if md5_value != auth_key:
            return self.set_response(**{'status': False, 'message': 'auth_key error', 'error_code': -1})

        # 过滤不安全的sql
        if 'update' in sql.strip()[:6].lower() and 'where' not in sql:
             return self.set_response(**{'status': False, 'message': 'invalied: update without where', 'error_code': -1})
        if 'delete' in sql.strip()[:6]:
            return self.set_response(**{'status': False, 'message': 'invalied: delete not support', 'error_code': -1})

        if sql_type == 'select':
            status, result = self.__sql_manage_api.select_info(sql)
            infos_list = [dict(row) for row in result]
            return self.set_response(**{'result': infos_list})

        else:
            status, result = self.__sql_manage_api.other_info(sql)
            return self.set_response(**{'result': result.rowcount})
