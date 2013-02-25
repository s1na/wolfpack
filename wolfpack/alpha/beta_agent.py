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
        is_finished = False
        while True:
            if not is_ready:
                status = self.conn.recv(10)
                if status != 'ready':
                    print 'Beta is not ready and says: '
                    print status
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

            self.conn.sendall("%s|%d|%d" % (chunk_info[1], chunk_info[2], chunk_info[3]))
            ok = int(self.conn.recv(1))
            if ok:
                is_ready = False
                total_bytes = chunk_info[3] - chunk_info[2]
                data = ''
                while len(data) < total_bytes:
                    part = self.conn.recv(512)
                    rest = ''
                    if not part:
                        print "V: Beta no data received."
                        break
                    else:
                        if 'END' in part:
                            print 'V: END exists in part'
                            part, rest = part[:part.index('END')], part[part.index('END'):]
                            if 'ready' in rest:
                                is_ready = True
                                rest = rest.replace('ready', '')
                            is_finished = True
                        if 'ready' in part:
                            print 'V: Ready in part!'
                        data = data + part + rest

                if not is_finished:
                    print 'V: Determining if correctly got END'
                    leftover = self.conn.recv(100)
                    print leftover
                    if 'END' in leftover:
                        print 'V: Got END'
                        leftover = leftover.replace('END', '')
                        if 'ready' in leftover:
                            is_ready = True
                    else:
                        print 'Beta didn\'t get END, instead got: '
                        print leftover 
                        continue

                file_name = "dls/%s.%s" % (chunk_info[1].split('/')[-1], chunk_info[4])
                f = open(file_name, 'wb')
                f.write(data)
                f.close()

                self.alpha.finished_chunk(chunk_info)
                is_finished = False

            else:
                print 'beta %d unsuccessful download'

