#!/usr/bin/python

import sys
import requests
import threading
import socket
import io


class AlphaThread(threading.Thread):
    def __init__(self, socket_, url, num, range_, file_name):
        threading.Thread.__init__(self)
        self.socket_ = socket_
        self.url = url
        self.num = num
        self.range_ = range_
        self.file_name = file_name

    def run(self):
        print 'waiting for beta %d' % self.num
        conn, addr = self.socket_.accept()
        print(addr)

        conn.sendall("%s,%d,%s" % (self.url, self.num, self.range_))

        ok = int(conn.recv(1))

        if ok:

            print 'beta %d -> waiting for data' % self.num
            f = open("%s.%s" % (self.file_name, self.num), 'wb')

            start, end = [int(item) for item in self.range_.split('-')]
            total_bytes = end - start
            data = ''

            for i in range((total_bytes / (4 * 1024)) + 1):
                data += conn.recv(4 * 1024)

            print 'got beta %ds data' % self.num
#                buffered_writer = io.BufferedWriter(f)
#                buffered_writer.write(data)
#                buffered_writer.close()
            f.write(data)
            f.close()
        else:
            print 'beta %d unsuccessful download'

        conn.close()


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


url = sys.argv[1]
file_name = url.split('/')[-1]
betas = int(sys.argv[2])

r = requests.head(url)
file_size = int(r.headers['content-length'])

ranges = calculate_ranges(betas, file_size)

if betas:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 54321))
    s.listen(betas)

    for i in range(1, betas + 1):
        t = AlphaThread(s, url, i, ranges[i], file_name)
        t.start()

print 'downloading my part'
r = requests.get(url, headers={'range': "bytes=%s" % ranges[0]})
print 'downloaded my part'
print r.headers

f = open("%s.0" % file_name, 'wb')
f.write(r.content)
f.close()

f = open(file_name, 'wb')
for i in range(betas + 1):
    f.write(open("%s.%d" % (file_name, i), 'rb').read())
f.close()
