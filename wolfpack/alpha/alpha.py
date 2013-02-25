#!/usr/bin/python

import sys
import socket
import io
import shutil
import requests
from wolfpack.alpha.listener import Listener
from wolfpack.alpha.dl_file import DLFile
from wolfpack.alpha.beta_agent import BetaAgent
from wolfpack.lib.utils import log
from wolfpack.alpha import settings

class Alpha(object):
    def __init__(self, max_beta_number = 20):
        self.betas = []
        self.dl_files = []  # Files to be downloaded
        self.downloaded_files = list()
        self.listener = Listener(self, max_beta_number)
        self.listener.start()

    def add_url(self, url):
        self.dl_files.append(DLFile(url))

    def add_beta(self, conn, addr):
        beta = BetaAgent(self, conn)
        self.betas.append(beta)
        beta.start()

    def request_chunk(self):
        if not self.dl_files:
            return (False, 'sleep')

        counter = 0
        res = self.dl_files[counter].request_chunk()
        while len(res) == 1 :
            if res[0] == 'Downloading':
                counter += 1
            elif res[0] == 'Downloaded':
                self.downloaded_files.append(
                    self.dl_files.pop(counter)
                )
            if not (counter < len(self.dl_files)):
                break
            res = self.dl_files[counter].request_chunk()
        if counter == len(self.dl_files):
            return (False, 'sleep')

        res.insert(0, True)
        return tuple(res)

    def finished_chunk(self, chunk_info):
        for dl_file in self.dl_files:
            if dl_file.url == chunk_info[1]:
                identifier = (chunk_info[2], chunk_info[3], chunk_info[4])
                dl_file.downloaded_chunks.append(
                    dl_file.downloading_chunks.pop(
                        dl_file.downloading_chunks.index(identifier)
                    )
                )
                if dl_file.check_status():  # If finished
                    self.finished_dl_file(dl_file)

    def finished_dl_file(self, dl_file):
        print 'I: The following has finished downloading:'
        print dl_file.url

        self.dl_files.remove(dl_file)

    def del_beta(self, beta):
        beta.conn.close()
        self.betas.remove(beta)

    def halt(self):
        for beta in self.betas:
            self.del_beta(beta)
        self.listener.stop = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', settings.PORT))
        sys.exit(0)

    def verify(self, data):
        pass


