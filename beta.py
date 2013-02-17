#!/usr/bin/python

import socket, requests, sys

HOST = '127.0.0.1'
PORT = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.settimeout(1)
s.connect((HOST, PORT))
data = s.recv(1024)

url, num, range_ = data.split(',')

r = requests.get(url, stream=True, headers={'range' : "bytes=%s" % range_})

ok = '1' if r.ok else '0'
data_file = r.raw

s.sendall(ok)


while True:
    data = data_file.read(4)
    print len(data)
    if not len(data):
        break
    else:
        try:
            s.sendall(data)
        except socket.error:
            print "Socket error"

s.close()
