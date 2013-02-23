#!/usr/bin/python

import requests
import wolfpack.alpha.settings as settings

class DLFile(object):
    def __init__(self, url):
        self.url = url
        self.name = self.url.split('/')[-1]
        self.chunks = list()

        r = requests.head(url)
        self.size = r.headers['content-length']
        self.headers = r.headers    # TODO: Is it needed?

        calculate_ranges()

    def calculate_ranges(self):
        if self.size < settings.CHUNK_SIZE:
            self.chunks.append("%d-%d" %(0, self.size - 1))  #just one part to download

        num_part = self.size / settings.CHUNK_SIZE
        for i in range(num_part):
            self.chunks.append(("%d-%d" %
                                (i * each_part,
                                 ((i + 1) * each_part) - 1))
                               ,"Available")
        self.chunks.append(("%d-%d" %
                            (num_part * each_part,
                             self.size - 1))
                           ,"Available")

    def request_chunk(self):
        for i in range(len(self.chunks)):
            if i[1] == "Available":
                start, end = [int(item) for item in i[0].split('-')]
                return (self.url, start, end, i)

    def merge_parts(self):
        pass
