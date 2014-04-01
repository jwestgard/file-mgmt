#!/usr/bin/env python3
    
local_set = set()
fedora_set = set()

# Read the contents of the *first column* of the first data file
# into the first set.
for line in open('prangeasset.txt'):
    local_set.add(line.rstrip("\n").split("\t")[0])

# Read the contents of the second file into the second set
for line in open('pcbinfedora.txt'):
    fedora_set.add(line.rstrip("\n"))
    
# Print out the number of items read for each of the data files  
print("\nList of unique local assets: {0} files".format(len(local_set)))
print("List of unique fedora assets: {0} files".format(len(fedora_set)))

# Compare the two sets and create new sets containing the files missing from  
# the other set.
not_local = fedora_set.difference(local_set)
not_in_fedora = local_set.difference(fedora_set)

# Print out the number of items in one set but not the other.
print("{0} files are not in fedora.".format(len(not_in_fedora)))
print("{0} files are not found in local copies.".format(len(not_local)))

# Save the results of the comparison to two files.
with open('results/not_prangeasset.txt', 'w') as f:
    f.writelines(x + "\n" for x in sorted(not_local))
with open('results/not_fedora.txt', 'w') as f:
    f.writelines(x + "\n" for x in sorted(not_in_fedora))
