#!/usr/bin/python

import socket
import time
import requests
import threading
#from wolfpack.lib.alpha_addr import get_alpha_addr
import wolfpack.beta.settings as settings

class Beta(object):
    def __init__(self):
        self.socket_ = None
        self.current_speed = 0.0
        self.current_file_lenght = 0
        self.connect()

    def connect(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        #self.socket_.connect(get_alpha_addr()) #TODO: I couldn't get nmap to work.
	self.socket_.connect((settings.HOST, settings.PORT))
        print 'Connected to the Alpha successfully.'
        print 'Waiting for further instructions.'
        #self.socket_.sendall("%s|%s"%(settings.USER, settings.PASS)) # verify username and password

        self.send_request()

    def receive(self):
        req = requests.get(self.curr_url, stream=True, headers={'range': "bytes=%s" % self.range_}) #to change for next version

        time.sleep(1)   # Wait for it to get a few bytes.

        ok = '1' if req.ok else '0'
        self.socket_.sendall(ok)

        #for repairing the reset by peer Error
        #I Broke package in 10 small package
        #and send It to Beta_agent
        pre_time = time.time();
        pack_size = settings.PACKAGE_SIZE / settings.PACKAGE_PEIS
        for packet in req.iter_content(chunk_size = settings.PACKAGE_SIZE):
            new_time = time.time()
            for i in range(settings.PACKAGE_PEIS):
                bytes_ = packet[i * pack_size: (i+1) * pack_size]
                self.socket_.sendall(bytes_)
            self.current_file_lenght += len(packet)
            self.current_speed = (settings.PACKAGE_SIZE / 1024.0 / (new_time - pre_time))  #KBps #        data_file = r.raw #        total_bytes = self.end - self.start
#
#        current = 0
#        while current < total_bytes:
#            data = data_file.read(512)
#            if not data:
#                break
#            self.socket_.sendall(data)
#            current+=512

	self.socket_.sendall('END')
        self.send_request()

    def send_request(self):
        self.socket_.sendall('ready')
        orders = self.socket_.recv(1024)   # Wait for orders   (url,start,end)
        if not orders:
                self.socket_.close()
                return
        while True:
            if "sleep" in orders:
                #time.sleep(60)
                orders = self.socket_.recv(1024)
            else:
                break
        self.curr_url, self.start, self.end = orders.split('|')
	self.start, self.end = int(self.start), int(self.end)
        self.range_ = self.end - self.start
        self.receive()

