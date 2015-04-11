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

from importlib import import_module
import yaml
import assemblyline

# TODO: JS minifier
# TODO: Remember to mention python-yaml and assemblyline in the dependencies
#       Also mention the dependencies for the various bundled processes
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


class Wembler:
    # The parameters for __init__ must reflect the attributes set through
    # argparse by the launcher script
    def __init__(self, config):
        if not isinstance(config, dict):
            with open(config, 'r') as cf:
                config = yaml.load(cf)
        workersN = config['max_threads']
        begin_inputs = config['begin_inputs']
        stations = {}
        for name in config['tasks']:
            taskconf = config['tasks'][name]
            pname = taskconf['process']
            inputname = taskconf['input']
            outputnames = taskconf['outputs']
            del taskconf['process']
            del taskconf['input']
            del taskconf['outputs']
            try:
                Process = import_module('.'.join(
                                    ('wembler.processes', pname))).Process
            except ImportError:
                Process = import_module('.'.join(
                                    ('assemblyline.processes', pname))).Process

            stations[name] = (Process(**taskconf), inputname, outputnames)
        self.factory = assemblyline.Factory(workersN, begin_inputs, stations)

    def build(self):
        self.factory.begin()
