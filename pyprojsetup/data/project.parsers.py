# -*- coding: UTF-8 -*-
"""
Parse command-line arguments.
"""

from __future__ import print_function

import argparse
# import json
import os
# import pkg_resources

from __init__ import __version__
from __init__ import DESCRIPTION

if __package__:
    # Installed version
    # Open any data files using pkg_resources, in case we are zipped
    # with pkg_resources.resource_stream(__package__, 'data/foo.json') as f:
    #    foo = json.load(f)
    PROG = __package__
else:
    # Development version, possibly unknown to pkg_resources
    # Open any data files from disk using os
    HERE = os.path.dirname(os.path.realpath(__file__))
    PROG = os.path.basename(HERE)
    # with open(os.path.join(HERE, 'data', 'foo.json')) as f:
    #    foo = json.load(f)


def add_parser(subparsers):
    """Hook for integrating this parser as a subparser in another program's
    parsers."""
    subparser = subparsers.add_parser(PROG, help=DESCRIPTION)
    _add_arguments(subparser)


def _add_arguments(subparser):
    """Define optional and required command-line arguments"""
    subparser.add_argument(
        "--version", action="version",
        help="show the version number and exit",
        version="{{}} {{}}".format(PROG, __version__)
    )
    # More arguments go here.


def main():
    """Return a parser containing command-line arguments.
    The object will still need to be parsed with parser.parse_args()
    Returning the unparsed object allows flexibility for other parsers
    to be added, preparsing, integration with argcomplete, etc."""
    parser = argparse.ArgumentParser(prog=PROG, description=DESCRIPTION)
    _add_arguments(parser)
    return parser
