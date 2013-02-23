#!/usr/bin/python

import threading
import socket
import beta_agent
import wolfpack.alpha.DLFile

class Listener(threading.Thread):
    def __init__(self, max_beta_number, alpha_obj):
        threading.Thread.__init__(self)
        self.socket_ = socket.socket(socket.AF_INIT, socket.SOCK_STREAM)
        self.socket_.bind(('', 54321))
        self.socket_.listen(max_beta_number)
        self.alpha = alpha_obj

    def run(self):
        while True:
            conn, addr = self.socket_.accept()
            self.alpha.add_beta(conn, addr)


