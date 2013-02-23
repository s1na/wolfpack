#!/usr/bin/python

import socket
import threading

class BetaAgent(threading.Thread):
    def __init__(self, socket_, url, num, range_, file_name):
        threading.Thread.__init__(self)
        self.socket_ = socket_
        self.url = url
        self.num = num
        self.range_ = range_
        self.file_name = file_name

    def run(self):
        print 'waiting for beta %d' % self.num
        conn, addr = self.socket_.accept()
        print(addr)

        conn.sendall("%s,%d,%s" % (self.url, self.num, self.range_))

        ok = int(conn.recv(1))

        if ok:

            print 'beta %d -> waiting for data' % self.num
            f = open("%s.%s" % (self.file_name, self.num), 'wb')

            start, end = [int(item) for item in self.range_.split('-')]
            total_bytes = end - start
            data = ''

            while len(data) < total_bytes:
                chunk = conn.recv(512)
                if not chunk:
                    print "No data received."
                    break
                data += chunk

            print 'got beta %ds data' % self.num
            f.write(data)
            f.close()
        else:
            print 'beta %d unsuccessful download'

        conn.close()


