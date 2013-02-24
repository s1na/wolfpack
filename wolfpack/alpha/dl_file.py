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
        counter = 0
        if self.size < settings.CHUNK_SIZE:
            self.available_chunks.append((0, self.size - 1, counter))  #just one part to download
            return

        num_part = self.size / settings.CHUNK_SIZE
        for i in range(num_part):
            self.available_chunks.append((i * settings.CHUNK_SIZE, 
                                          ((i + 1) * settings.CHUNK_SIZE) - 1), counter)
            counter += 1
        if not self.size % settings.CHUNK_SIZE:
            self.available_chunks.append((num_part * settings.CHUNK_SIZE,
                                          self.size - 1), counter)

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
        final_file = open(self.name, 'wb')
        for i in range(len(self.downloaded_chunks)):
            shutil.copyfileobj(open("%s.%d" % (self.name, i), 'rb'), final_file)
        final_file.close()

