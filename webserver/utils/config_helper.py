# -*- coding: utf-8 -*-

__author__ = 'wgs@test'

import os
import yaml


class _Config(object):
    __config = None

    def load_config_file(self, path):
        with open(path, 'r') as f:
            self.__config = yaml.safe_load(f)

    @property
    def data(self):
        return self.__config

    def get(self, accessor_string, default_val=None):
        current_data = self.__config
        paths = accessor_string.split('.')
        for chunk in paths:
            if current_data and chunk in current_data:
                current_data = current_data[chunk]
            else:
                return default_val
        return current_data

    # def test(self):
    #     print(self.__config)

config = _Config()
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'etc', 'default.yml')

def load_all_config():
    config.load_config_file(config_path)

# config_path = os.path.join('F:\C.2\京东\9nserver\etc', 'default.yml')
# print(config_path)
# load_all_config()
# config.test()
