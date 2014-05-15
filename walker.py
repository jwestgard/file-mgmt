#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime, os, sys, json, subprocess

def count_by_ext(files):
    result = {}
    for f in files:
        ext = os.path.splitext(f)[1][1:]
        if ext in result.keys():
            result[ext] += 1
        else:
            result[ext] = 1
    return result

def exec_shell_command(i, f):
    cmd = ['exiftool', '-j', '-filetype', '-filesize', '-XResolution',
           '-YResolution', '-imagewidth', '-imageheight', f]
    # print out the shell commands being run on each file as they are run
    print("{0}:".format(i+1), " ".join([x for x in cmd]))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    j = p.communicate()[0].decode("utf-8")
    result = json.loads(j)[0]
    return result

def filter_by_ext(files, ext):
    result = []
    for f in files:
        if f.endswith(ext):
            result.append(f)
        else:
            pass
    return result

def filter_completed_dirs(dirs, completed_dirs):
    return [d for d in dirs if d not in completed_dirs]

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

def listfiles(path, filter_ext):
    result = []
    for root, dirs, files in os.walk(path):
        print("\n", root)
        # prune directories beginning with dot
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        # prune files beginning with dot
        files[:] = [f for f in files if not f.startswith('.')]
        try:
            files = filter_by_ext(files, filter_ext)
        except IndexError:
            pass
        for f in files:
            print("  •", f)
            result.append(os.path.join(root, f))
    return result

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def modification_time(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def pretty_print(table):
    number_cols = max([len(line) for line in table])
    column_width = max([len(str(cell)) for row in table for cell in row])
    table_width = 2 + (number_cols * column_width) + ((number_cols - 1) * 3)
    border =  "═" * table_width
    print("\n╔" + border + "╗")
    # This line prints generic column numbers as the header row
    # header = ["COL {0}".format(x) for x in range(1, (number_cols + 1))]
    # This line uses the values in the first row of the data as the header
    header = table.pop(0)
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

def report_on_directory(root, d, outdir):
    fullpath = os.path.join(root, d)
    print("\nChecking the following directory: {0} ...".format(fullpath))
    # output file path
    out_temp = os.path.join(outdir, 'temp.txt')
    out_final = os.path.join(outdir, '{0}.txt'.format(d))
    # metadata items to report on each file
    header = ['fullpath', 'bytes', 'modtime', 'XResolution',
              'YResolution', 'ImageWidth', 'ImageHeight']
    # print full list of files arranged by subdirs
    filelist = listfiles(fullpath, filter_ext)
    total_bytes = 0
    
    with open(out_temp, 'a+') as outfile:
        outfile.write("\t".join([x.upper() for x in header]) + "\n")
        print("\nPerforming metadata analysis on {0} files ...\n".format(len(filelist)))
        for i, f in enumerate(filelist):
            result = [f]                            # filename
            bytes = os.path.getsize(f)
            result.append(bytes)                    # bytes
            total_bytes += bytes
            result.append(modification_time(f))     # modification time
            imagemeta = exec_shell_command(i,f)     # get image metadata from exiftool
            for m in ['XResolution', 'YResolution', 
                      'ImageWidth', 'ImageHeight']: 
                try:
                    result.append(imagemeta[m])     # append these four values or
                except KeyError:
                    result.append("[none]")         # 'none' if not available
            outfile.write("\t".join([str(r) for r in result]) + "\n")
    
    print("\nTotal: {0} bytes, or {1} for {2} files.".format(total_bytes,
                                                             human_readable_size(total_bytes),
                                                             len(filelist)))
    counts = count_by_ext(filelist)
    count_display = ", ".join(".{0} ({1})".format(k, counts[k]) for k in sorted(counts.keys()))
    print("Extensions: {0}".format(count_display))
    print("Completed scan of", fullpath)
    print("Moving {0} to {1}".format(out_temp, out_final))
    os.rename(out_temp, out_final)
    
if __name__ == "__main__":
    searchroot = os.path.abspath(sys.argv[1])
    outpath = os.path.abspath(sys.argv[2])
    filter_ext = sys.argv[3]
    print("\n*** FILE REPORTER ***")
    print("Search path = ", searchroot)
    print("Storing results in ", outpath)
    alldirs = [i for i in os.listdir(searchroot) if os.path.isdir(os.path.join(searchroot, i))]
    completed_dirs = [os.path.splitext(n)[0] for n in os.listdir(outpath)]

    dirs_to_search = filter_completed_dirs(alldirs, completed_dirs)
    for d in dirs_to_search:
        print("\nDirectory listing progress:")
        print("===========================")
        for dir in alldirs:
            print(dir.ljust(25), dir in completed_dirs)
        report_on_directory(searchroot, d, os.path.dirname(outpath))
        