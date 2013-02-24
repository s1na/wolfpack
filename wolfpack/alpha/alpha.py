#!/usr/bin/python

import sys
import socket
import io
import shutil
import requests
from wolfpack.alpha.listener import Listener
from wolfpack.alpha.dl_file import DLFile
from wolfpack.alpha.beta_agent import BetaAgent

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

    def request_chunk(self):
        counter = 0
        res = self.dl_files[counter].request_chunk()
        while len(res) != 3:
            if res[0] == "Downloading":
                counter += 1
            elif res[0] == "Downloaded":
                self.downloaded_files.append(
                    self.dl_files.pop(counter)
                )
            res = self.dl_files[counter].request_chunk()
        return res

    def del_beta(self, conn):
        conn.close()
        for beta in self.betas:
            if beta[0] == conn:
                self.betas.remove(beta)

    def halt(self):
        self.listener.stop = True

    def verify(self, data):
        pass

#url = sys.argv[1]
#file_name = url.split('/')[-1]
#betas = int(sys.argv[2])

#r = requests.head(url)
#file_size = int(r.headers['content-length'])

#ranges = calculate_ranges(betas, file_size)

#threads = []
#if betas:
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind(('', 54321))
    #s.listen(betas)

    #for i in range(1, betas + 1):
        #t = AlphaThread(s, url, i, ranges[i], file_name)
        #threads.append(t)
        #t.start()

#print 'downloading my part'
#r = requests.get(url, headers={'range': "bytes=%s" % ranges[0]})
#print 'downloaded my part'
#print r.headers

#f = open("%s.0" % file_name, 'wb')
#f.write(r.content)
#f.close()

## Wait for all the threads to finish.
#for t in threads:
    #t.join()

