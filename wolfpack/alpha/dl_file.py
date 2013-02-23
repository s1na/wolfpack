#!/usr/bin/python

import requests

class DLFile(object):
    def __init__(self, url):
        self.url = url
        self.name = self.url.split('/')[-1]
        self.parts = 0
        self.ranges = list()

        r = requests.head(url)
        self.size = r.headers['content-length']
        self.headers = r.headers    # TODO: Is it needed?

    def calculate_ranges(self):
        if not self.parts:
            return []

        each_part = self.size / self.parts
        for i in range(self.parts):
            if i != self.parts - 1:
                self.ranges.append("%d-%d" %
                              (i * each_part,
                               ((i + 1) * each_part) - 1)
                             )
            else:
                self.ranges.append("%d-%d" %
                              (i * each_part,
                               self.size - 1)
                             )
        return self.ranges

    def merge_parts(self):
        pass
