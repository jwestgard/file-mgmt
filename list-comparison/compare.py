#!/usr/bin/env python3

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
    
local_set = set()
fedora_set = set()

for line in open('all_prange_filenames_with_paths.txt'):
    local_set.add(line.rstrip("\n").split("\t")[0])

for line in open('all_prange-pcbinfedora.txt'):
    fedora_set.add(line.rstrip("\n"))
    
print("\nList of unique local assets: {0} files".format(len(local_set)))
print("List of unique fedora assets: {0} files".format(len(fedora_set)))

not_local = fedora_set.difference(local_set)
not_in_fedora = local_set.difference(fedora_set)

print("{0} files are not in fedora.".format(len(not_in_fedora)))
print("{0} files are not found in local copies.".format(len(not_local)))

with open('not_local.txt', 'w') as f:
    f.writelines(x + "\n" for x in sorted(not_local))
    
with open('not_in_fedora.txt', 'w') as f:
    f.writelines(x + "\n" for x in sorted(not_in_fedora))
    
alignedlists = alignlists(local_set, fedora_set)

with open('aligned.tsv', 'w') as f:
    f.writelines(x + "\n" for x in alignedlists)
    
