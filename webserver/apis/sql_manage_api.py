#!/usr/bin/env python3
# Time: 2018/12/6 18:46

__author__ = 'wgs@test'



# import climate
import traceback
# logging = climate.get_logger(__name__)

from db.db import db_session_manager as session_manager
from apis.base_api import BaseApi

class SqlManageApi(BaseApi):

    def __init__(self):
        super(BaseApi, self).__init__()

    def select_info(self, sql):
        with session_manager.with_session() as session:
            db = session
            try:
                res = db.execute(sql)
                info = res.fetchall()
                return True, info
            except Exception as e:
                err_msg = '[Faild exec sql]:\n %s , err info: %s', sql, traceback.format_exc()
                raise Exception(err_msg)

    def other_info(self, sql):
        with session_manager.with_session() as session:
            db = session
            try:
                info = db.execute(sql)
                db.commit()
                return True, info
            except Exception as e:
                err_msg = '[Faild exec sql]:\n %s , err info: %s', sql, traceback.format_exc()
                raise Exception(err_msg)