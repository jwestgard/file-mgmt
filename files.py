#!/usr/bin/env python

from __future__ import print_function
import os, sys

def listfiles(path):
    for root, dirs, files in os.walk(path):
        result = []
        # prune directories beginning with dot
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        # prune files beginning with dot
        files[:] = [f for f in files if not f.startswith('.')]
        # if a extension filter has been specified, invoke function to prune files lacking that extension
        try:
            files[:] = filter_by_ext(files, sys.argv[2])
        except IndexError:
            pass
        for f in files:
            path = os.path.join(root, f)
            bytes = os.path.getsize(path)
            result.append(path, bytes)
    return result
    
def filter_by_ext(files, ext):
    result = []
    for f in files:
        if f.endswith(ext):
            result.append(f)
        else:
            pass
    return result

def human_readable_size(b):
    bytes = int(b)
    print("Bytes: {0}".format(bytes))
    if bytes >= 2**40:
        return "{0} TB".format(round(bytes / 2**40), 2)
    elif bytes >= 2**30:
        return "{0} GB".format(round(bytes / 2**30), 2)
    elif bytes >= 2**20:
        return "{0} MB".format(round(bytes / 2**20), 2)
    else:
        return "{0} KB".format(round(bytes / 2**10), 2)

def main():
    print("Checking {0} ...".format(sys.argv[1]))
    searchroot = os.path.dirname(sys.argv[1])
    print(searchroot)
    listfiles(searchroot)
    
if __name__ == "__main__":
    main()
