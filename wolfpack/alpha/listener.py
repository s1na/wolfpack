#!/usr/bin/python

import threading
import socket
import beta_agent
from wolfpack.alpha.dl_file import DLFile
import wolfpack.alpha.settings as settings

class Listener(threading.Thread):
    def __init__(self, alpha, max_beta_number):
        threading.Thread.__init__(self)
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_.bind(('', 54328))#settings.PORT))
        self.socket_.listen(max_beta_number)
        self.alpha = alpha
        self.stop = False

    def run(self):
        while not self.stop:
            conn, addr = self.socket_.accept()
            if addr == '127.0.0.1':  # Time for halt.
                continue

            self.alpha.add_beta(conn, addr)

        self.socket_.close()

