# -*- coding: UTF-8 -*-
"""
Parse command-line arguments.
"""

from __future__ import print_function

import argparse
import getpass
import json
import os
import pkg_resources

from __init__ import __version__
from __init__ import DESCRIPTION

if __package__:
    # Installed version
    # Open any data files using pkg_resources, in case we are zipped
    with pkg_resources.resource_stream(__package__,
                                       'data/githubconfig.json') as f:
        githubconfig = json.load(f)
    PROG = __package__
else:
    # Development version
    # Open any data files using os
    path = os.path.dirname(os.path.realpath(__file__))
    PROG = os.path.basename(path)
    with open(os.path.join(path, 'data', 'githubconfig.json')) as f:
        githubconfig = json.load(f)

githosts = [g["hostname"] for g in githubconfig]


def add_parser(subparsers):
    p = subparsers.add_parser(
        PROG,
        help=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    _add_arguments(p)


def _add_arguments(subparser):
    subparser.add_argument(
        "--version", action="version",
        help="show the version number and exit",
        version="{} {}".format(PROG, __version__)
    )
    subparser.add_argument(
        '--author',
        help='author name(s) for package metadata '
        '(default: system username)',
        default=getpass.getuser()
        )
    subparser.add_argument(
        '--email', default="author@example.com",
        help='author e-mail address for package metadata '
        '(default: author@example.com)'
        )
    subparser.add_argument(
        '--startingversion',
        help='starting version number (default: 0.1)',
        default="0.1"
        )
    subparser.add_argument(
        '--github', choices=githosts, default="github.com",
        help='specify the github that will host this project '
        '(default: github.com)'
        )
    subparser.set_defaults(
        githubconfig=githubconfig
        )
    subparser.add_argument(
        'name',
        help="project name"
        )
    subparser.add_argument(
        'path', nargs='?',
        help=(
            "location where the project root directory will be created "
            "(default: current directory)"),
        default=os.getcwd()
        )
    subparser.add_argument(
        '--description', default="Bar foo-er for humans",
        help="Short, one-line description of the project "
        "(default: Bar foo-er for humans)"
        )
    subparser.add_argument(
        '--organization', default=getpass.getuser(),
        help="The github organization or user that will own the project "
        "(default: system username)"
        )
    subparser.add_argument(
        '--packages', nargs='+',
        help="extra packages to pip install in the new virtual environment"
        )


def main():
    parser = argparse.ArgumentParser(
        prog=PROG,
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    _add_arguments(parser)
    return parser
