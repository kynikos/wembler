#!/usr/bin/env python3

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
from . import subprocesses


class FileLoader:
    def __init__(self, basedir):
        self.basedir = basedir

    def process(self, dummy):
        for fname in os.listdir(self.basedir):
            if os.path.isfile(os.path.join(self.basedir, fname)):
                yield (fname, )


class HTMLContent:
    # TODO: JS minifier
    def __init__(self, template_dir, url_prefix, css_dir, css_style,
                 output_dir):
        self.jinja = subprocesses.Jinja(template_dir, url_prefix, output_dir)
        self.sass = subprocesses.Sass(template_dir, url_prefix, css_dir,
                                      css_style)

    def process(self, template):
        css = self.sass.compile(template)
        self.jinja.render(template, css)
        yield ()
