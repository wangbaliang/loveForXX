#!/usr/bin/env python3
# Time: 2018/10/29 15:54

__author__ = 'wgs@test'


from utils.config_helper import config
from utils.alarm import http_alarm
# import climate
# logging = climate.get_logger(__name__)



class NineAlarm(object):
    def __init__(self):
        self.now_name = '9n_server'
        self.now_env = config.get('now_env')

    def alarm(self, task, error_msg):
        alarm_info = 'pin: %s task_id:%s algo_name:%s task_name: %s task_type:%s.  err:%s' % (
            task.user_name, task.task_id, task.algo_name, task.task_name, task.task_type, error_msg)
        # logging.info('报警问题: %s' % alarm_info)
        http_alarm(alarm_info, now_env=self.now_env, now_name=self.now_name)
        return True
