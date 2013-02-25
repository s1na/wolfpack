#!/usr/bin/python

import os, sys, inspect

 # realpath() with make your script run, even if you symlink it :)
splitted_path = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]).split('/')
del splitted_path[-2:]
joined_path = os.path.join(*splitted_path)
cmd_folder = os.path.realpath(joined_path)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)
