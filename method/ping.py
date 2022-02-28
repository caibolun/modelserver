#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 21:56:32
LastEditTime: 2022-02-28 23:42:32
'''
from ModelServer.handler import Handler
import logging

class Ping(Handler):
    def __init__(self, cfg, busi_cfg, file_logger=None, ppid=None, sockets=None):
        Handler.__init__(self, cfg, busi_cfg, file_logger, ppid, sockets)
        self.logger = logging.getLogger()
        self.model = None

    def env_init(self):
        pass

    def apply(self, req):
        resp = req
        return resp

