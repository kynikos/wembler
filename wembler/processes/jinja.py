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

import os.path
from jinja2 import Environment, FileSystemLoader


class Process:
    def __init__(self, inputdir, outputdir, base_prefix):
        self.env = Environment(loader=FileSystemLoader(inputdir),
                               trim_blocks=True, lstrip_blocks=True,
                               autoescape=True)
        self.outputdir = outputdir
        self.base_prefix = base_prefix

    def process(self, item):
        page, css = item
        base_url = os.path.join(self.base_prefix, page) \
                   if self.base_prefix else None
        self.env.get_template(page).stream(
            css=css,
            page=page,
            base_url=base_url,
        ).dump(os.path.join(self.outputdir, os.path.basename(page)))
        yield ()
