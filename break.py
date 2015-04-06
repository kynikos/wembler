#!/usr/bin/env python

import sys

fname = sys.argv[1]
LEN = 79
TAB = 4


def split_line(line):
    rlen = LEN - TAB
    split = line.split(" ")
    newline = split[0]
    for word in split[1:]:
        newnewline = " ".join((newline, word))
        if TAB + len(newnewline) < LEN:
            newline = newnewline
        else:
            yield " " * TAB + newline + "\n"
            newline = word
    else:
        yield " " * TAB + newline + "\n"

with open(fname, "r") as stream:
    output = ""
    for line in stream.readlines():
        for newline in split_line(line[:-1]):
            output += newline

with open(fname, "w") as stream:
    stream.write(output)
