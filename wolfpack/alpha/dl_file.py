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
        if  self.size < settings.CHUNK_SIZE:
            return []   # Files under CHUNK_SIZE are not allowed.

        each_part = self.size / settings.CHUNK_SIZE
        for i in range(self.parts + 1):
            if i != self.parts - 1:
                self.chunks.append(("%d-%d" %
                              (i * each_part,
                               ((i + 1) * each_part) - 1)
                                   ),
                                   "Available"
                                  )
            else:
                self.chunks.append(("%d-%d" %
                              (i * each_part,
                               self.size - 1)
                                   ),
                                   "Available"
                                  )
                                  

    def request_chunk(self):
        for i in range(len(self.chunks)):
            if i[1] == "Available":
                start, end = [int(item) for item in i[0].split('-')]
                return (self.url, start, end, i)

    def merge_parts(self):
        pass
