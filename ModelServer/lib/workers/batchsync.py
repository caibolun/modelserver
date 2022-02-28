#coding=utf-8

import os
import errno
import socket
import select

from ModelServer.lib.utils import close_on_exec
from ModelServer.lib.workers.base import Worker

__all__ = ["BatchSyncWorker"]


class BatchSyncWorker(Worker):

    def receive_one(self, timewait):
        ret = select.select(self.rd_fds, [], [], timewait)
        if ret[0]:
            try:
                for sock in ret[0]:
                    client, addr = sock.accept()
                    client.setblocking(1)
                    close_on_exec(client)
                    return sock, client, addr
            except socket.error as e:
                if e.args[0] not in (errno.EAGAIN, errno.ECONNABORTED,
                        errno.EWOULDBLOCK):
                    client.close()
                    #self.rd_fds.remove(client)
                    raise
        return None

    def run(self):
        super(BatchSyncWorker, self).run()
        if self.LISTENERS:
            while self.alive:
                socks = []
                clients = []
                addrs = []
                res = self.receive_one(1.0)
                if res is not None:
                    socks.append(res[0])
                    clients.append(res[1])
                    addrs.append(res[2])
                    for i in range(self.batch_size - 1):
                        res = self.receive_one(5.0/1000)
                        if res is not None:
                            socks.append(res[0])
                            clients.append(res[1])
                            addrs.append(res[2])
                        else:
                            break
                    self.handle_request(socks, clients, addrs)

                if self.ppid != os.getppid():
                    self.file_logger.info("Parent changed, shutting down: %s", self)
                    return

                self.nr += 1
                if self.nr > self.max_requests:
                    self.alive = False

        else:
            while self.alive:
                self.handle_request()
                self.nr += 1
                if self.nr > self.max_requests:
                    self.alive = False
