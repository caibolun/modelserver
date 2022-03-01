#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 22:42:55
LastEditTime: 2022-03-01 12:12:55
'''
import logging
import pickle
from .lib.workers.sync import SyncWorker
import struct

class Handler(SyncWorker):
    def __init__(self, cfg, file_logger=None, ppid=None, sockets=None):
        SyncWorker.__init__(self, cfg, file_logger, ppid, sockets)
        self.logger = logging.getLogger()

    def init_process(self):
        super(Handler, self).init_process()

    def stop(self):
        super(Handler, self).stop()

    def apply(self, req_buff):
        raise RuntimeError('apply UnImplement')

    def env_init(self):
        self.logger.info("env_init UnImplement")
        pass

    def run(self):
        self.env_init()
        super(Handler, self).run()

    def handle_request(self, sock, client, addr):
        self.logger.info("handler_request")
        pack_head_net_data = client.recv(4)
        recv_packpkg_len = struct.unpack('!I',pack_head_net_data)
        pack_head_net_data = b'' 
 
        while recv_packpkg_len[0] != len(pack_head_net_data):
            packet = client.recv(1024 * 16 * 8)
            pack_head_net_data += packet
 
        try:
            ret = 0 
            xargs, kwargs = pickle.loads(pack_head_net_data)
            res = self.apply(*xargs, **kwargs)
            respBuff = pickle.dumps(res)
        except Exception as e:
            ret = -1
            respBuff = b'' 
            self.logger.error("%s", e)
 
        packLen = 4 + 4 + len(respBuff)
        headerPkg = struct.pack('!I', packLen)
        retPkg = struct.pack('!i', ret)
        try:
            client.send(headerPkg)
            client.send(retPkg)
            client.send(respBuff)
        except Exception as e:
            self.logger.error("%s", e)
