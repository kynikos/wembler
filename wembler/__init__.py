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
# TODO: Remember to mention python-yaml and assemblyline in the dependencies
import yaml
import assemblyline
# TODO: Make the following dependencies optional
import jinja2
# Documentation: http://hongminhee.org/libsass-python/
# TODO: Contribute support for the .sass (indented) syntax
import sass
# TODO: See also https://github.com/Kronuz/pyScss
#       import scss


class Wembler:
    # The parameters for __init__ must reflect the attributes set through
    # argparse by the launcher script
    def __init__(self, config, debug=False):
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
        stations = SimpleStaticWebsite(url_prefix, css_style)
        self.factory = assemblyline.Factory(WORKERS, stations)

    def build(self):
        self.factory.begin()


def SimpleStaticWebsite(url_prefix, css_style):
    TEMPLATE_DIR = './templates'
    return (
        (_Loader(
            basedir=TEMPLATE_DIR,
         ), None, ('templates', )),
        (_SimpleStaticWebsite(
            template_dir=TEMPLATE_DIR,
            url_prefix=url_prefix,
            css_dir='./scss',
            css_style=css_style,
            output_dir='www',
         ), 'templates', ()),
    )


class _Loader:
    def __init__(self, basedir):
        self.basedir = basedir

    def process(self, dummy):
        for fname in os.listdir(self.basedir):
            if os.path.isfile(os.path.join(self.basedir, fname)):
                yield (fname, )


class _SimpleStaticWebsite:
    # TODO: JS minifier
    def __init__(self, template_dir, url_prefix, css_dir, css_style,
                 output_dir):
        self.url_prefix = url_prefix
        self.css_dir = css_dir
        self.css_style = css_style
        self.output_dir = output_dir
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True
        )

    def process(self, template):
        css = self._compile_scss(template)
        self._compile_jinja(template, css)
        yield ()

    def _compile_scss(self, template):
        fname = os.path.splitext(template)[0]
        scssf = ".".join((fname, "scss"))
        return sass.compile(filename=os.path.join(self.css_dir, scssf),
                            output_style=self.css_style,
                            custom_functions={
                                sass.SassFunction('relurl', ('$url', ),
                                                  self._relurl),
                            })

    def _relurl(self, url):
        return "url('{}')".format(os.path.join(self.url_prefix,
                                               self.dequote(url)))

    def _compile_jinja(self, template, css):
        base_url = os.path.join(self.url_prefix, template) \
                   if self.url_prefix else None
        self.jinja_env.get_template(template).stream(
            css=css,
            page=template,
            base_url=base_url,
        ).dump(os.path.join(self.output_dir, os.path.basename(template)))

    @staticmethod
    def dequote(string):
        # TODO: Move to more generic library
        if string[0] == string[-1] and string.startswith(("'", '"')):
            return string[1:-1]
        return string
