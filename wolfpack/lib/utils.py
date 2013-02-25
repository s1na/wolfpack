#!/usr/bin/python

def log(text):
    f = open('log', 'a')
    f.write(text)
    f.close()
