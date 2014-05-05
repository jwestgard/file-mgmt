#!/usr/bin/env python3
    
def alignlists(list1, list2):
    result = []
    col1 = iter(sorted(list1))
    col2 = iter(sorted(list2))
    x = next(col1)
    y = next(col2)
    while col1 and col2:
        if x == None and y == None:
            break
        elif x == None:
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
        else:
            print("Something went wrong!")
            break
    return result

local_set = set()
fedora_set = set()

for line in open('prangeasset.txt'):
    local_set.add(line.rstrip("\n").split("\t")[0])

for line in open('pcbinfedora.txt'):
    fedora_set.add(line.rstrip("\n"))
                 
result = alignlists(local_set, fedora_set)

for i in result:
    print(i)
