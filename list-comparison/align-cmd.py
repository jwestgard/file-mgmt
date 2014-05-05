#!/usr/bin/env python3

import sys

def filetolist(filename):
    result = []
    with open(filename) as f:
        for line in f:
            cols = line.split(".")
            result.append(cols[0].rstrip("\n"))
    return result

def alignlists(list1, list2):
    col1 = iter(sorted(list1))
    col2 = iter(sorted(list2))
    x = next(col1)
    y = next(col2)
    result = []    
    while col1 and col2:
        if x == None and y == None:
            break
        if x == None:
            while y:
                result.append("\t" + str(y))
                y = next(col2, None)
        elif y == None:
            while x:
                result.append(str(x) + "\t")
                x = next(col1, None)
        elif x == y:
            result.append(str(x) + "\t" + str(y))
            x = next(col1, None)
            y = next(col2, None)
        elif x > y:
            result.append("\t" + str(y))
            y = next(col2, None)
        elif x < y:
            result.append(str(x) + "\t")
            x = next(col1, None)
    return result

a = filetolist(sys.argv[1])
b = filetolist(sys.argv[2])

result = alignlists(a,b)
for line in result:
    print(line)
