#!/usr/bin/python

import shutil
import os
import requests
import wolfpack.alpha.settings as settings

class DLFile(object):
    def __init__(self, url):
        self.url = url
        self.name = self.url.split('/')[-1]

        self.available_chunks = list()
        self.downloaded_chunks = list()
        self.downloading_chunks = list()

        r = requests.head(url)
        self.size = int(r.headers['content-length'])
        self.headers = r.headers    # TODO: Is it needed?

        self.calculate_ranges()
        self.num_part=0 #count chunks

    def calculate_ranges(self):
        counter = 0
        if self.size < settings.CHUNK_SIZE:
            self.available_chunks.append((0, self.size - 1, counter))  #just one part to download
            return

        num_part = self.size / settings.CHUNK_SIZE
        for i in range(num_part):
            self.available_chunks.append((i * settings.CHUNK_SIZE, 
                                          ((i + 1) * settings.CHUNK_SIZE) - 1, counter))
            counter += 1
        if self.size % settings.CHUNK_SIZE > 0:
            self.available_chunks.append((num_part * settings.CHUNK_SIZE,
                                          self.size - 1, counter))

    def request_chunk(self):
        if not len(self.available_chunks):
            if not len(self.downloading_chunks):
                self.merge_parts()
                return ["Downloaded",]
            else:
                return ["Downloading",]

        print 'available'
        item = self.available_chunks[0]
        self.downloading_chunks.append(self.available_chunks.pop(0))
        return [self.url, item[0], item[1], item[2]]


    def merge_parts(self):
        final_file = open('dls/' + self.name, 'wb')
        for i in range(len(self.downloaded_chunks)):
            file_name = "dls/%s.%d" % (self.name, i)
            shutil.copyfileobj(open(file_name, 'rb'), final_file)
            os.remove(file_name)
        final_file.close()

    def check_status(self):
        if not len(self.available_chunks) and\
           not len(self.downloading_chunks):
            self.merge_parts()
            return True # If finished
        return False
