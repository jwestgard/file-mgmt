#!usr/bin/env python3

#
# Automated checksum validation of files against checksums 
# stored in a text file.
#
# usage --> python3 cksum-compare.py [dirlist.txt] [path/to/files/]
#

import csv, os, sys
import hashlib

def walkdirs(dir):
    for dirpath, dnames, fnames in os.walk(dir):
    	for f in fnames:
    		print("{0}\t{1}".format(f, dirpath))

def listfiles(directory):
    files = os.listdir(directory)
    for f in files:
        cksum = md5(f)
        print(f, "=", cksum)
 
def md5(filename):
    hasher = hashlib.md5()
    with open(filename, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def main():
    myfile = sys.argv[1]
    mydir = sys.argv[2]
    
    with open(myfile, 'r') as f:
        archived_files = csv.DictReader(f, delimiter='\t', quotechar='"')
        for item in archived_files:
            checksum_filename = mydir + item['Key'] + ".md5"
            with open(checksum_filename, 'r') as csfile:
                orig_checksum = csfile.read().strip('\n')
                if item['Data'] == orig_checksum:
                    print(item['Data'], orig_checksum, "OK")
                else:
                    print(item['Data'], orig_checksum, "BAD")
        
main()
