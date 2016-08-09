#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Main module of {}. Provides command-line entry point and main logic.
"""


def main(args=None):
    """CLI entry point"""
    if not args:
        import parsers
        parser = parsers.main()
        args = parser.parse_args()


if __name__ == '__main__':
    main()
