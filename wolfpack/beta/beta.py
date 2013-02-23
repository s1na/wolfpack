#!/usr/bin/python

import socket
import time
import requests
import wolfpack.beta.settings as settings

class Beta(object):
    def __init__(self):
        self.socket_ = None

        connect()

    def connect(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.connect((settings.HOST, settings.PORT))

        orders = self.socket_.recv(1024)   # Wait for orders
        if orders == "sleep":
            # TODO: test again 5 mins later, or wait for the alpha to wake him up?

        else:
            self.curr_url, self.range_ = data.split('|')
            receive()

    def receive(self):
        r = requests.get(self.curr_url, stream=True, headers={'range': "bytes=%s" % self.range_})
        time.sleep(1)   # Wait for it to get a few bytes.

       	#TODO: stream and send to BetaAgent


        ok = '1' if r.ok else '0'
       	data_file = r.raw
       	start, end = [int(item) for item in range_.split('-')]
        total_bytes = end - start

        self.socket_.sendall(ok)

        current = 0
        while current < total_bytes:
            data = data_file.read(512)
            if not data:
                break

            chunk = self.socket_.sendall(data)[current:])
            current += 512 

