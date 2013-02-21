#!/usr/bin/python

import socket
import time
import requests

#HOST = '127.0.0.1'
HOST = "172.17.9.98"
PORT = 54321

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(1024)
url, num, range_ = data.split(',')
r = requests.get(url, stream=True, headers={'range': "bytes=%s" % range_})
time.sleep(2)

ok = '1' if r.ok else '0'
data_file = r.raw
start, end = [int(item) for item in range_.split('-')]
total_bytes = end - start

s.sendall(ok)

current = 0
while current < total_bytes:
    data = data_file.read(512)
    if not data:
        break

    chunk = s.sendall(data)#[current:])
    current += 512 

#total_bytes_sent = 0
#while True:
    #data = data_file.read(4)
    #if not len(data):
        #break
    #else:
        #bytes_sent = 0
        #while bytes_sent < 4 * 1024: 
            #stage_sent = 0
            #try:
                ##stage_sent = s.send(data[bytes_sent:])
                #stage_sent = s.send("haha")
                #if stage_sent == 0:
                    #print 'no bytes sent'
                #bytes_sent += stage_sent

            #except socket.error, e:
                #print "Socket error, %s" % e

s.close()
