#!/usr/bin/env python

from __future__ import print_function

import os, sys
from PIL import Image

def listfiles(path):
    result = []
    # counter for adding up total bytes
    totalbytes = 0
    print("Checking {0} ...".format(path))
    for root, dirs, files in os.walk(path):
        # prune directories beginning with dot
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        # prune files beginning with dot
        files[:] = [f for f in files if not f.startswith('.')]
        # if a extension filter has been specified, invoke function to prune files lacking that extension
        try:
            files[:] = filter_by_ext(files, sys.argv[2])
        except IndexError:
            pass
        # for each file remaining, get size in byes, list filename, path, bytes
        for f in files:
            path = os.path.join(root, f)
            dpi = get_dpi(path)
            bytes = os.path.getsize(path)
            result.append("{0}\t{1}\t{2}".format(path, bytes, dpi))
            totalbytes += bytes
    return result, totalbytes
    
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

def get_dpi(filename):
    img = Image.open(filename)
    metadata = img.info
    try:
        result = metadata['dpi']
    except:
        result = "Not found"
    return result

def main():
    try:
        ext = sys.argv[2]
    except IndexError:
        ext = "all"
    filelist, sizeinbytes = listfiles(sys.argv[1])
    with open('result.txt', 'w') as f:
        for x in filelist:
            print(x)
            f.write("{0}\n".format(x))
    print("Done! {0} files found with extension '{1}'.".format(len(filelist), ext))
    print("Total size of {0} files = {1}.".format(ext, human_readable_size(sizeinbytes)))
    
if __name__ == "__main__":
    main()
