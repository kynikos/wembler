# Wembler - Progressive website assembler.
# Copyright (C) 2015 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Wembler.
#
# Wembler is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wembler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wembler.  If not, see <http://www.gnu.org/licenses/>.

import os
# Documentation: http://hongminhee.org/libsass-python/
# TODO: Contribute support for the .sass (indented) syntax
import sass
# TODO: See also https://github.com/Kronuz/pyScss
#       import scss


class Process:
    def __init__(self, inputdir, outputdir, urlprefix, style):
        self.inputdir = inputdir
        self.outputdir = outputdir
        self.urlprefix = urlprefix or ""
        self.style = style

    def process(self, item):
        # TODO: This should be generalized...
        fname = os.path.splitext(item)[0]
        scssf = ".".join((fname, "scss"))
        cssf = ".".join((fname, "css"))
        css = sass.compile(filename=os.path.join(self.inputdir, scssf),
                           output_style=self.style,
                           custom_functions={
                                sass.SassFunction('relurl', ('$url', ),
                                                  self._relurl),
                            })
        with open(os.path.join(self.outputdir, cssf), 'w') as of:
            of.write(css)

        yield (item, )

    def _relurl(self, url):
        return "url('{}')".format(os.path.join(self.urlprefix,
                                               self.dequote(url)))

    @staticmethod
    def dequote(string):
        # TODO: Move to separate module
        if string[0] == string[-1] and string.startswith(("'", '"')):
            return string[1:-1]
        return string
