#!/usr/bin/python

import threading
import socket
import beta_agent
import wolfpack.alpha.DLFile

class Listener(threading.Thread):
    def __init__(self, alpha, max_beta_number):
        threading.Thread.__init__(self)
        self.socket_ = socket.socket(socket.AF_INIT, socket.SOCK_STREAM)
        self.socket_.bind(('', 54321))
        self.socket_.listen(max_beta_number)
        self.alpha = alpha
        self.stop = False

    def run(self):
        while not self.stop:
            conn, addr = self.socket_.accept()
            self.alpha.add_beta(conn, addr)

        self.socket_.close()

