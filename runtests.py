#!/usr/bin/env python

import doctest
import sys

py3k = sys.version_info >= (3, 0)

if py3k:
    num_failures, num_tests = doctest.testfile('docs/quickstart_python3.txt')
else:
    num_failures, num_tests = doctest.testfile('docs/quickstart.txt')

if num_failures > 0:
    print("%d failures out of %d tests" % (num_failures, num_tests))
    sys.exit(1)

sys.exit(0)
