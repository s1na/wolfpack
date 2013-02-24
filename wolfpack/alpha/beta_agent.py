#!/usr/bin/python

import socket
import threading
import time
from wolfpack.alpha.dl_file import DLFile
from wolfpack.lib.utils import log

class BetaAgent(threading.Thread):
    def __init__(self, alpha, conn):
        threading.Thread.__init__(self)
        self.alpha = alpha
        self.conn = conn

    def run(self):
        is_ready = False
        while True:
            if not is_ready:
                print 'not ready'
                status = self.conn.recv(10)
                if status != 'ready':
                    print 'Beta is not ready!'
                    break
                is_ready = True

            chunk_info = self.alpha.request_chunk()  # (url, start, end, num)
			#if not self.alpha.verify(self.conn.recv(1024).split('|'))
			#	break

            if not chunk_info[0]:
                self.conn.sendall(chunk_info[1])
                time.sleep(2)
                continue

            if not len(chunk_info):
                break

            print chunk_info
            self.conn.sendall("%s|%d|%d" % (chunk_info[1], chunk_info[2], chunk_info[3]))
            ok = int(self.conn.recv(1))
            if ok:
                is_ready = False
                print 'beta ok'
                total_bytes = chunk_info[3] - chunk_info[2]
                data = ''
                while len(data) < total_bytes:
                    part = self.conn.recv(512)
                    rest = ''
                    if not part:
                        print "No data received."
                        break
                    else:
                        if 'END' in part:
                            part, rest = part[:part.index('END')], part[part.index('END'):]
                            self.alpha.finished_chunk(chunk_info)
                        if "ready" in rest:
                            is_ready = True
                        data += part 
                f = open("%s.%s" % (chunk_info[1].split('/')[-1], chunk_info[4]), 'wb')
                f.write(data)
                f.close()

            else:
                print 'beta %d unsuccessful download'

