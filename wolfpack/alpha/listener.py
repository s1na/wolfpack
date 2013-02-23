#!/usr/bin/python

import threading
import socket
import beta_agent
import wolfpack.alpha.DLFile

class Listener(threading.Thread):
    def __init__(self, max_beta_number, alpha_obj):
        threading.Thread(self)
        self.socket_ = socket.socket(socket.AF_INIT, socket.SOCK_STREAM)
        self.socket_.bind(('', 54321))
        self.socket_.listen(max_beta_number)
        self.betas = []
        self.alpha = alpha_obj

    def run(self):
        while True:
            conn, addr = self.socket_.accept()
            self.betas.append(self.alpha.add_beta(conn, addr))

    def del_beta(self, conn):
        conn.close()
        for beta in self.betas:
            if beta[0] == conn:
                del beta

