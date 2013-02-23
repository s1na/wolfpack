#!/usr/bin/python

import socket
import threading
from wolfpack.alpha.listener import Listener
from wolfpack.alpha.dl_file import DLFile

class BetaAgent(threading.Thread):
    def __init__(self, alpha, conn):
        threading.Thread.__init__(self)
        self.alpha = alpha
        self.conn = conn

    def run(self):
        while True:
            chunk_info = self.alpha.request_chunk()  # (url, start, end, num)
            if not len(chunk_info):
                break

            self.conn.sendall("%s|%d|%d" % (chunk_info[0], chunk_info[1], chunk_info[2]))
            ok = int(self.conn.recv(1))
            if ok:
                total_bytes = chunk_info[2] - chunk_info[1]
                data = ''
                while len(data) < total_bytes:
                    part = self.conn.recv(512)
                    if not part:
                        print "No data received."
                        break
                    data += part 

                f = open("%s.%s" % (chunk_info[0].split('/')[-1], chunk_info[3]), 'wb')
                f.write(data)
                f.close()
            else:
                print 'beta %d unsuccessful download'

        self.alpha.listener.del_beta(conn)

