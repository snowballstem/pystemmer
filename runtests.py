#!/usr/bin/env python

import sys, doctest

py3k = sys.version_info >= (3, 0)

if py3k:
    num_failures, num_tests = doctest.testfile('docs/quickstart_python3.txt')
else:
    num_failures, num_tests = doctest.testfile('docs/quickstart.txt')

sys.exit(num_failures)
