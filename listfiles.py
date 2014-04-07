#!/usr/bin/env python3

import os
import sys

def listfiles(dir):
    result = []
    print("Checking {0}".format(dir))
    for path, dnames, fnames in os.walk(dir):
        print(path)
        for f in fnames:
#           print("{0}\t{1}\t{2}".format(f, os.path.getsize(os.path.join(path, f)), path))
            result.append(f)
    return result
    
def listjpgs(files):
	result = []
	for f in files:
		if f.endswith(".jpg"):
			result.append(f)
	return result

def main():
    allfiles = listfiles(sys.argv[1])
    jpgs = listjpgs(allfiles)
    with open('KAPjpgfiles.txt', 'w') as f:
        for x in jpgs:
            print(x)
            f.write("{0}\n".format(x))
    print("Done! {} JPEG files found.".format(len(jpgs)))
    
if __name__ == "__main__":
    main()
