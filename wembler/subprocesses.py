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

    def render(self, template, title, content, css, outfile):
        base_url = os.path.join(self.url_prefix, outfile) \
                   if self.url_prefix else None
        self.env.get_template(template).stream(
            title=title,
            content=content,
            css=css,
            page=template,
            base_url=base_url,
        ).dump(os.path.join(self.output_dir, os.path.basename(outfile)))


class Sass:
    # Documentation: http://hongminhee.org/libsass-python/
    # TODO: Contribute support for the .sass (indented) syntax
    # TODO: See also https://github.com/Kronuz/pyScss
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
    # TODO: Try https://github.com/lepture/mistune
    def __init__(self, article_dir):
        self.article_dir = article_dir

        def url_builder(label, base, end):
            # TODO: implement
            return base + label + end

        self.md = markdown.Markdown(
            output_format='html5',
            tab_length=4,
            enable_attributes=False,
            smart_emphasis=True,
            lazy_ol=False,
            # See https://pythonhosted.org/Markdown/extensions/index.html
            # for configuration options
            extensions=['markdown.extensions.extra',
                        # 'extra' includes the following extensions:
                        #'markdown.extensions.abbr',
                        #'markdown.extensions.attr_list',
                        #'markdown.extensions.def_list',
                        #'markdown.extensions.fenced_code',
                        #'markdown.extensions.footnotes',
                        #'markdown.extensions.tables',
                        #'markdown.extensions.smart_strong',
                        'markdown.extensions.admonition',
                        'markdown.extensions.codehilite',
                        'markdown.extensions.meta',
                        'markdown.extensions.nl2br',
                        'markdown.extensions.sane_lists',
                        'markdown.extensions.smarty',
                        'markdown.extensions.toc',
                        'markdown.extensions.wikilinks'],
            extension_configs={
                'markdown.extensions.toc': {
                    'title': 'Table of contents:',
                    # TODO: Note how e.g. Sphinx makes the para symbol appear
                    #       only when hovering over the heading!
                    'permalink': True,
                    # TODO: set the 'slugify' option for a custom function to
                    #       generate anchors
                },
                'markdown.extensions.wikilinks': {
                    'build_url': url_builder,
                }
            },
        )

    def convert(self, article):
        with open(os.path.join(self.article_dir, article), 'r') as stream:
            self.md.reset()
            # TODO: Find a better way to automatically add a ToC
            text = '[TOC]\n\n' + stream.read()
            return self.md.convert(text)


class TitleFound(UserWarning):
    def __init__(self, data):
        self.data = data


class TitleFinder(html.parser.HTMLParser):
    # TODO: TitleFinder should be replaced with a Markdown extension
    #       https://pythonhosted.org/Markdown/extensions/api.html
    def __init__(self):
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_data(self, data):
        if self.current_tag == 'h1':
            raise TitleFound(data)
