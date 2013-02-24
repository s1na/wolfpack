import os, sys, inspect
 # realpath() with make your script run, even if you symlink it :)
splitted_path = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]).split('/')
del splitted_path[-1]
joined_path = '/'.join(splitted_path)
cmd_folder = os.path.realpath(joined_path)
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

#cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
#if cmd_subfolder not in sys.path:
    #sys.path.insert(0, cmd_subfolder)


execfile('alpha/alpha.py', {})

