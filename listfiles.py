#!/usr/bin/env python3

import os
import sys

def listfiles(dir):
    for path, dnames, fnames in os.walk(dir):
    	for f in fnames:
    		print("{0}\t{1}\t{2}".format(f, os.path.getsize(os.path.join(path, f)), path))

def main():
    listfiles(sys.argv[1])
    
if __name__ == "__main__":
    main()
