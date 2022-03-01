#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 22:49:54
LastEditTime: 2022-03-01 12:27:49
'''
#encoding=utf-8
import configparser

from ModelServer.lib.singleton import Singleton

class Config(object):
    """use singleton avoid global variables"""
    __metaclass__ = Singleton

    def __init__(self, config_file, section_name="DEFAULT"):
        self._cfg = configparser.ConfigParser()
        self._cfg.read([config_file, ])
        self.section_name = section_name

    def get(self, option, section=None, value_type=str):
        return self._cfg._get(section or self.section_name, value_type, option)

    def __getattr__(self, option):
        try:
            return self.get(option)
        except Exception as e:
            return None

