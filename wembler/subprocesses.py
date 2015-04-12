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

import os.path
import html.parser

# TODO: Make the following dependencies optional
import jinja2
import sass
# TODO: See also https://github.com/Kronuz/pyScss
#       import scss
import markdown


class Jinja:
    # Documentation: http://jinja.pocoo.org/docs/dev/api/
    def __init__(self, template_dir, url_prefix, output_dir):
        self.url_prefix = url_prefix
        self.output_dir = output_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True
        )

    def render(self, template, css):
        base_url = os.path.join(self.url_prefix, template) \
                   if self.url_prefix else None
        self.env.get_template(template).stream(
            css=css,
            page=template,
            base_url=base_url,
        ).dump(os.path.join(self.output_dir, os.path.basename(template)))


class Sass:
    # Documentation: http://hongminhee.org/libsass-python/
    # TODO: Contribute support for the .sass (indented) syntax
    def __init__(self, template_dir, url_prefix, css_dir, css_style):
        self.url_prefix = url_prefix
        self.css_dir = css_dir
        self.css_style = css_style

    def compile(self, template):
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

    @staticmethod
    def dequote(string_):
        # TODO: Move to more generic library
        if string_[0] == string_[-1] and string_.startswith(("'", '"')):
            return string_[1:-1]
        return string_


class Markdown:
    # Documentation: https://pythonhosted.org/Markdown/reference.html
    #                https://pythonhosted.org/Markdown/extensions/index.html
    def __init__(self, article_dir):
        self.article_dir = article_dir
        self.md = markdown.Markdown()  # TODO: See the available options and
                                       #       extensions

    def convert(self, article):
        with open(os.path.join(self.article_dir, article), 'r') as stream:
            self.md.reset()
            return self.md.convert(stream.read())


class TitleFound(UserWarning):
    def __init__(self, data):
        self.data = data


class TitleFinder(html.parser.HTMLParser):
    def __init__(self):
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_data(self, data):
        if self.current_tag == 'h1':
            raise TitleFound(data)
