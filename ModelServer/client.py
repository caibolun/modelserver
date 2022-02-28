#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 23:00:33
LastEditTime: 2022-02-28 23:04:44
'''
import socket
import struct
import logging
import select
import pickle
import time

class Client(object):
    def __init__(self, timeout = 3):
        self.sockets = {}
        self.timeout = timeout
        self.logger = logging.getLogger()

    def createSocket(self, key):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(key)
        return s

    def getAny(self, key):
        return self.createSocket(key)

    def recv_timeout(self, sock, bytes_to_read, timeout_seconds):
        sock.setblocking(0)
        ready = select.select([sock], [], [], timeout_seconds)
        if ready[0]:
            return sock.recv(bytes_to_read)

        raise socket.timeout()

    def call(self, func, *args, **kwargs):
        ret = -1
        try:
            st = time.time()
            s = self.getAny(func)
            reqBuff = pickle.dumps((args,kwargs))
            lens = len(reqBuff)
            headPkg = struct.pack('!I', lens)
            s.send(headPkg)
            s.send(reqBuff)
            time_del = int((time.time() - st) * 1000)
            self.logger.info("send to model size: <%u> cost %u ms", len(headPkg + reqBuff), time_del)
            st = time.time()
            byte = self.recv_timeout(s, 4, self.timeout)
            lens = struct.unpack('!I', byte)[0]
            byte = self.recv_timeout(s, 4, self.timeout)
            ret = struct.unpack('!i', byte)[0]
            respBuff = b''
            while len(respBuff) != lens - 8:
                byte = self.recv_timeout(s, 1024 * 16 * 8, self.timeout)
                respBuff += byte
            time_del = int((time.time() - st) * 1000)
            self.logger.info("recv to model cost %u ms", time_del)
            return ret, pickle.loads(respBuff)
        except Exception as e:
            import traceback
            self.logger.info('call fail %s %s', traceback.format_exc(), e)
        return ret, None

