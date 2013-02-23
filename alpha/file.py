#!/usr/bin/python

class File(object):
    def __init__(self):
        pass

    def calculate_ranges(betas, file_size):
        each_part = file_size / (betas + 1)
        ranges = list()
        for i in range(betas + 1):
            if i != betas:
                ranges.append("%d-%d" %
                              (i * each_part,
                               ((i + 1) * each_part) - 1)
                             )
            else:
                ranges.append("%d-%d" %
                              (i * each_part,
                               file_size - 1)
                             )
        return ranges


