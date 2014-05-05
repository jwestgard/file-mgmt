#!/usr/bin/env python3

c1 = 0
c2 = 0
file_assets = []
fedora_assets = []
result = []
result2 = []

for line in open('prangeasset.txt'):
    cols = line.rstrip("\n").split("\t")
    file_assets.append(cols[0])

for line in open('pcbinfedora.txt'):
    fedora_assets.append(line.rstrip("\n"))
    
print("\nTotal File Assets: {0} files".format(len(file_assets)))
print("Totel Fedora Assets: {0} files".format(len(fedora_assets)))

print("\nComparing the two lists of files ...")

result1 = []
for row in file_assets:
    if row[0] not in fedora_assets:
        c1 += 1
        print("File {0} not found: {1}".format(c1, row[0]))
        result.append(row[0])

result2 = []
for row[0] in fedora_assets:
    if row not in file_assets:
        c2 += 1
        print("File {0} not found: {1}".format(c2, row))
        result2.append(row)

with open('files.txt', 'w') as f:
    f.writelines(x + "\n" for x in sorted(result))
    
with open('fedora.txt', 'w') as f:
    f.writelines(x + "\n" for x in sorted(result2))

print("Found {0} files not in Fedora.".format(c1))
print("Found {0} files in Fedora not stored locally.".format(c2))
