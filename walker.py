#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, sys, json, subprocess

def count_by_ext(files):
    result = {}
    for f in files:
        ext = os.path.splitext(f)[1][1:]
        if ext in result.keys():
            result[ext] += 1
        else:
            result[ext] = 1
    return result

def exec_shell_command(f):
    cmd = ['exiftool', '-j', '-filetype', '-filesize', '-XResolution', '-YResolution', '-imagewidth', '-imageheight', f]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    j = p.communicate()[0].decode("utf-8")
    result = json.loads(j)[0]
    del result['SourceFile']
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
    if bytes >= 2**40:
        return "{0} TB".format(round(bytes / 2**40), 2)
    elif bytes >= 2**30:
        return "{0} GB".format(round(bytes / 2**30), 2)
    elif bytes >= 2**20:
        return "{0} MB".format(round(bytes / 2**20), 2)
    else:
        return "{0} KB".format(round(bytes / 2**10), 2)

def listfiles(path):
    result = []
    for root, dirs, files in os.walk(path):
        print("\n", root)
        # prune directories beginning with dot
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        # prune files beginning with dot
        files[:] = [f for f in files if not f.startswith('.')]
        try:
            files = filter_by_ext(files, sys.argv[2])
        except IndexError:
            pass
        for f in files:
            metadata = {}
            print("  •", f)
            metadata['filename'] = f
            metadata['fullpath'] = os.path.join(root, f)
            metadata['bytes'] = os.path.getsize(metadata['fullpath'])
            result.append(metadata)
    return result

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def write_report(data):
    result = []
    for item in data:
        line =[]
        for x in ['filename', 'bytes', 'XResolution', 'YResolution']:
            try:
                line.append(item[x])
            except KeyError:
                line.append("[none]")
        result.append(line)
    return result        

def pretty_print(table):
    number_cols = max([len(line) for line in table])
    column_width = max([len(str(cell)) for row in table for cell in row])
    table_width = 2 + (number_cols * column_width) + ((number_cols - 1) * 3)
    border =  "═" * table_width
    print("\n╔" + border + "╗")
    header = ["COL {0}".format(x) for x in range(1, (number_cols + 1))]
    print("║ {0} ║".format(" ╎ ".join(cell.center(column_width) for cell in header)))
    print("╟" + "━" * table_width + "╢")
    for row in table:
        cols = []
        while len(row) < number_cols:
            row.append("[null]")
        for cell in row:
            if is_number(cell):
                cols.append(str(cell).rjust(column_width))
            elif cell == "[none]":
                cols.append(cell.center(column_width))
            else:
                cols.append(cell.ljust(column_width))
        print("║ {0} ║".format(" ╎ ".join(col for col in cols)))
    print("╚" + border + "╝\n")
    
def pretty_print_dict(data):
    result = []
    col_widths = {}
    allkeys = []   
    for d in data:
        allkeys.extend(d.keys())
    cols = set(allkeys)
    for c in cols:
        col_widths[c] = len(c)
        for row in data:
            if c in row.keys():
                if len(str(row[c])) > col_widths[c]:
                    col_widths[c] = len(str(row[c]))
            else:
                row[c] = "N/A"
    table_width = 2 + sum(col_widths.values()) + ((len(cols) - 1) * 3)
    border = "═" * table_width
    print("\n╔" + border + "╗")
    headings = [h.upper().center(col_widths[h]) for h in cols]
    print("║ {0} ║".format(" ╎ ".join(headings)))
    print("╟" + "━" * table_width + "╢")
    for row in data:
        line = []
        for c in cols:
            try:
                if is_number(row[c]):
                    line.append(str(row[c]).rjust(col_widths[c]))
                else:
                    line.append(str(row[c]).ljust(col_widths[c]))
            except IndexError:
                line.append("N/A".center(col_widths[c]))
        print("║ {0} ║".format(" ╎ ".join(x for x in line)))
    print("╚" + border + "╝\n")

def total_bytes(files):
    return sum(f['bytes'] for f in files)
    
def main():
    searchroot = os.path.dirname(sys.argv[1])
    print("\n\n*** FILE REPORTER ***")
    print("\nChecking the following directory: {0} ...".format(searchroot))
    filelist = listfiles(searchroot)
    for f in filelist:
        additional_meta = exec_shell_command(f['fullpath'])
        f.update(additional_meta)
    total = total_bytes(filelist)
    print("\nTotal: {0} bytes, or {1} for {2} files.".format(
        total, human_readable_size(total), len(filelist)))
    counts = count_by_ext([f['filename'] for f in filelist])
    count_display = ", ".join(".{0} ({1})".format(
        k, counts[k]) for k in sorted(counts.keys()))
    print("Extensions: {0}\n".format(count_display))
    report = write_report(filelist)
    pretty_print(report)
    pretty_print_dict(filelist)

if __name__ == "__main__":
    main()