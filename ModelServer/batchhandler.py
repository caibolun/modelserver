#!/usr/bin/env python
# coding=utf-8
'''
Author: ArlenCai
Date: 2022-02-28 23:07:45
LastEditTime: 2022-02-28 23:07:46
'''
import time
import logging
import pickle
from ModelServer.lib.workers.batchsync import BatchSyncWorker
import struct

class BatchHandler(BatchSyncWorker):
    def __init__(self, cfg, busi_cfg, file_logger=None, ppid=None, sockets=None):
        BatchSyncWorker.__init__(self, cfg, busi_cfg, file_logger, ppid, sockets)
        self.logger = logging.getLogger()

    def init_process(self):
        super(BatchHandler, self).init_process()

    def stop(self):
        super(BatchHandler, self).stop()

    def apply(self, req_buff):
        raise RuntimeError('apply UnImplement')

    def env_init(self):
        self.logger.info("env_init UnImplement")
        pass

    def run(self):
        self.env_init()
        super(BatchHandler, self).run()

    def recv_timeout(self, sock, bytes_to_read, timeout_seconds):
        sock.setblocking(0)
        ready = select.select([sock], [], [], timeout_seconds)
        if ready[0]:
            return sock.recv(bytes_to_read)

        raise socket.timeout()

    def handle_request(self, socks, clients, addrs):
        self.logger.info("handler_request clients %s", str(clients))
        self.logger.info("handler_request addrs %s", str(addrs))
        st = time.time()
        reqs = []
        for client, addr in zip(clients, addrs):
            self.logger.info("handler_request client: <%s> addr: <%s>", client, addr)
            pack_head_net_data = client.recv(4)#self.recv_timeout(client, 4, 2)#client.recv(4)
            recv_packpkg_len = struct.unpack('!I',pack_head_net_data)
            pack_head_net_data = b''
            while recv_packpkg_len[0] != len(pack_head_net_data):
                packet = client.recv(1024 * 16 * 8)#self.recv_timeout(client, 1024 * 16 * 8, 2)#client.recv(1024 * 16 * 8)
                pack_head_net_data += packet
            time_del = int((time.time() - st)*1000)
            self.logger.info("cost %u ms", time_del)
            try:
                req = pickle.loads(pack_head_net_data)
            except Exception as e:
                self.logger.info("handler_request syserr %s", str(e))
                req = ()
            self.logger.info("handler_request pack_head_net_data: <%u>", len(pack_head_net_data))
            reqs.append(req)
        time_del = int((time.time() - st)*1000)
        self.logger.info("cost %u ms", time_del)
        try:
            ret = 0
            Ress = self.apply(reqs)
        except Exception as e:
            ret = -3
            Ress = [None] * len(clients)
            import traceback
            self.logger.info('handler_request apply fail %s %s', traceback.format_exc(), e)

        self.logger.info("handler_request client: <%u> rspsize: <%u>", len(clients), len(Ress))
        for res, client, addr in zip(Ress, clients, addrs):
            self.logger.error(" client %s", client)
            respBuff = pickle.dumps(res)
            packLen = 4 + 4 + len(respBuff)
            headerPkg = struct.pack('!I', packLen)
            retPkg = struct.pack('!i', ret)
            try:
                client.send(headerPkg)
                client.send(retPkg)
                client.send(respBuff)
            except Exception as e:
                self.logger.error("handler_request send fail %s", e)
