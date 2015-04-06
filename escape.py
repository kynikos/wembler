#!/usr/bin/env python

import sys
import html

fname = sys.argv[1]

with open(fname, "r") as stream:
    escaped = stream.read()

    escaped = html.escape(escaped)

    escnoamp = html.entities.entitydefs
    del escnoamp["amp"]

    for transl in escnoamp:
        escaped = escaped.replace(html.entities.entitydefs[transl],
                                  "&{};".format(transl))

    escaped = escaped.encode('ascii', 'xmlcharrefreplace')

with open(fname, "wb") as stream:
    stream.write(escaped)
