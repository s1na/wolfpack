#!/usr/bin/python

import socket, requests, sys

HOST = '127.0.0.1'
PORT = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.settimeout(1)
s.connect((HOST, PORT))
data = s.recv(1024)

url, num, range_ = data.split(',')

r = requests.get(url, headers={'range' : "bytes=%s" % range_})

ok = '1' if r.ok else '0'
data = r.content

s.sendall(ok)


i = 0
for i in range(0, len(data), 4 * 1024):
    if i + 4 * 1024 < len(data):
        s.sendall(data[i:i + 4 * 1024])
    else:
        s.sendall(data[i:])

s.close()
