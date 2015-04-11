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
from wembler import Wembler


def _parse_cli_args():
    cliparser = argparse.ArgumentParser(description=
            "Wembler - Progressive website assembler", add_help=True)
    cliparser.add_argument('-c', '--config', action='store',
                default='./wembler.yaml', type=str, metavar='FILE',
                help='the path to the configuration file '
                     '(default: %(default)s)')
    return vars(cliparser.parse_args())

Wembler(**_parse_cli_args()).build()
