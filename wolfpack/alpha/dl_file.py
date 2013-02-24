#!/usr/bin/python

import shutil
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

    def calculate_ranges(self):
        if self.size < settings.CHUNK_SIZE:
            self.available_chunks.append("%d-%d" %(0, self.size - 1))  #just one part to download

        num_part = self.size / settings.CHUNK_SIZE
        for i in range(num_part):
            self.available_chunks.append((i * settings.CHUNK_SIZE, 
                                          ((i + 1) * settings.CHUNK_SIZE) - 1))
        if not self.size % settings.CHUNK_SIZE:
            self.available_chunks.append((num_part * settings.CHUNK_SIZE,
                                          self.size - 1))

    def request_chunk(self):
        for item in self.available_chunks:
            self.downloading_chunks.apend(
                self.available_chunks.pop(self.available_chunks.index(item))
            )
            return (self.url, item[0], item[1])

        if not len(self.available_chunks):
            if not len(self.downloaded_chunks):
                self.merge_parts()
                return ("Downloaded",)
            else:
                return ("Downloading",)


    def merge_parts(self):
        final_file = open(self.name, 'wb')
        for i in range(betas + 1):
            shutil.copyfileobj(open("%s.%d" % (self.name, i), 'rb'), final_file)
        final_file.close()

