#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

data = [{"fullname": "Bob", "address": "Main Street", "phone": "301-555-4444"},
    {"fullname": "Joe", "address": "Oak Street", "phone": "301-555-6666"},
    {"fullname": "Steve", "address": "Yale Street", "phone": "301-555-5555",
     "spouse": "Sally"}]

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def pretty_print(table):
    number_cols = max([len(line) for line in table])
    column_width = max([len(cell) for row in table for cell in row])
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
                cols.append(cell.rjust(column_width))
            elif cell == "[null]":
                cols.append(cell.center(column_width))
            else:
                cols.append(cell.ljust(column_width))
        print("║ {0} ║".format(" ╎ ".join(col for col in cols)))
    print("╚" + border + "╝\n")
    
def pretty_print_dict(data):
    result = []
    col_widths = {}
    cols = reduce(set.union, (set(d.keys()) for d in data))
    for c in cols:
        col_widths[c] = len(c)
        for row in data:
            if c in row.keys():
                if len(row[c]) > col_widths[c]:
                    col_widths[c] = len(row[c])
            else:
                row[c] = "N/A"
    table_width = 2 + sum(col_widths.values()) + ((len(cols) - 1) * 3)
    border = "═" * table_width
    print("\n╔" + border + "╗")
    headings = [h.upper().center(col_widths[h]) for h in sorted(cols)]
    print("║ {0} ║".format(" ╎ ".join(headings)))
    print("╟" + "━" * table_width + "╢")
    for row in data:
        line = []
        for c in sorted(cols):
            try:
                line.append(row[c].ljust(col_widths[c]))
            except IndexError:
                line.append("N/A".center(col_widths[c]))
        print("║ {0} ║".format(" ╎ ".join(x for x in line)))
    print("╚" + border + "╝\n")
    
pretty_print_dict(data)
