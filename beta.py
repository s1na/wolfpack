#!/usr/bin/python

import socket, requests, sys

#HOST = '127.0.0.1'
HOST = "172.17.9.253"
PORT = 54325

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.settimeout(1)
s.connect((HOST, PORT))
data = s.recv(1024)

url, num, range_ = data.split(',')

#r = requests.get(url, stream=True, headers={'range' : "bytes=%s" % range_})

#ok = '1' if r.ok else '0'
#data_file = r.raw
ok = '1'
total_bytes = start - end = [int(item) for item in range_.split('-')]

s.sendall(ok)

total = 0
current = 0
while current < total_bytes:
    chunk = s.send(512 * "h")
    if not chunk:
        print "Beta: no data sent."
        break

    current += chunk

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
