#!/usr/bin/python

import socket
import time
import requests
import threading
from wolfpack.lib.alpha_addr import get_alpha_addr
import wolfpack.beta.settings as settings

class Beta(object):
    def __init__(self):
        self.socket_ = None
        self.current_speed = 0.0
        self.current_file_lenght = 0
        self.connect()

    def connect(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.connect(get_alpha_addr())
        #self.socket_.sendall("%s|%s"%(settings.USER, settings.PASS)) # verify username and password

        orders = self.socket_.recv(1024)   # Wait for orders   (url,start,end)
        if orders == "sleep":
            # TODO: test again 5 mins later, or wait for the alpha to wake him up?
            pass

        else:
            self.curr_url, self.start, self.end = orders.split('|')
            self.range_ = end - start
            self.receive()

    def receive(self):
        req = requests.get(self.curr_url, stream=True, headers={'range': "bytes=%s" % self.range_}) #to change for next version

        time.sleep(1)   # Wait for it to get a few bytes.

        ok = '1' if req.ok else '0'
        self.socket_.sendall(ok)

        pre_time = time.time();
        for packet in req.iter_content(chunk_size = settings.PACKAGE_SIZE):
            if not packet:
                break
            new_time = time.time()
            self.current_speed = (settings.PACKAGE_SIZE / (new_time - pre_time))
            self.socket_.sendall(packet)
            pre_time = new_time
            self.current_file_lenght += settings.PACKAGE_SIZE
        
        
        #data_file = r.raw
        #total_bytes = end - start


        #current = 0
        #while current < total_bytes:
            #data = data_file.read(512)
            #if not data:
                #break
            #self.socket_.sendall(data)
            #current+=512

if __name__ == '__main__':
    execfile('../lib/add_path.py', {})
    beta = Beta()
