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

import argparse
from wembler import Wembler, Wiklog


def _parse_cli_args():
    cliparser = argparse.ArgumentParser(description=
            "Wiklog - Experimental hybrid between a static blog and a "
            "personal wiki", add_help=True)
    cliparser.add_argument('-c', '--config', action='store',
                default='./wiklog.yaml', type=str, metavar='FILE',
                help='the path to the configuration file '
                     '(default: %(default)s)')
    cliparser.add_argument('--debug', action='store_true',
                help='enable debug mode')
    return vars(cliparser.parse_args())

Wembler(Wiklog, **_parse_cli_args()).build()
