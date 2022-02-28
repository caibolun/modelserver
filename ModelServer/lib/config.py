#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 22:49:54
LastEditTime: 2022-02-28 22:49:54
'''
#encoding=utf-8

import os
import configparser

from ModelServer.lib.singleton import Singleton

class Config(object):
    """use singleton avoid global variables"""
    __metaclass__ = Singleton

    DEFAULT_CONFIG_FILE = None
    ACTUAL_CONFIG_FILE = None
    SECTION_NAME = 'main'
    def __init__(self):
        self.load_config()

    def load_config(self):
        config_file = self.__class__.ACTUAL_CONFIG_FILE or self.__class__.DEFAULT_CONFIG_FILE
        self._cfg = configparser.ConfigParser()
        self._cfg.read([config_file, ])

    def get(self, option, section=None, value_type=str):
        return self._cfg._get(section or self.__class__.SECTION_NAME, value_type, option)

    def __getattr__(self, option):
        try:
            return self.get(option)
        except Exception as e:
            return None

if __name__ == '__main__':
    print (Config().get('base_path'))
