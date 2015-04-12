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

# TODO: Remember to mention python-yaml and assemblyline in the dependencies
import yaml
import assemblyline
from . import processes


class Wembler:
    # The parameters for __init__ must reflect the attributes set through
    # argparse by the launcher script
    def __init__(self, Model, config, debug=False):
        # TODO: Make more values configurable
        # TODO: Allow using custom processes from a local folder
        #     test = """
        #     import sys
        #
        #     b = 3
        #     c = 2
        #
        #     def aaa():
        #         return b + c
        #     """
        #
        #     namespace = {}
        #     exec(test, namespace)
        #     print(namespace["aaa"]())
        if not isinstance(config, dict):
            with open(config, 'r') as cf:
                config = yaml.load(cf)
        WORKERS = 12
        if debug:
            url_prefix = ''
            css_style = 'nested'
        else:
            url_prefix = config['url_prefix']
            css_style = 'compressed'
        stations = Model(url_prefix, css_style)
        self.factory = assemblyline.Factory(WORKERS, stations)

    def build(self):
        self.factory.begin()


def SimpleStatic(url_prefix, css_style):
    TEMPLATE_DIR = './templates'
    return (
        (processes.FileLoader(
            basedir=TEMPLATE_DIR,
         ), None, ('templates', )),
        (processes.HTMLContent(
            template_dir=TEMPLATE_DIR,
            url_prefix=url_prefix,
            css_dir='./scss',
            css_style=css_style,
            output_dir='www',
         ), 'templates', ()),
    )
