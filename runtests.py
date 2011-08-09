#!/usr/bin/env python

import sys, doctest

py3k = sys.version_info >= (3, 0)

if py3k:
    doctest.testfile('docs/quickstart_python3.txt')
else:
    doctest.testfile('docs/quickstart.txt')
