#!/usr/bin/env python

import doctest
import sys

num_failures, num_tests = doctest.testfile('docs/quickstart.txt')

if num_failures > 0:
    print("%d failures out of %d tests" % (num_failures, num_tests))
    sys.exit(1)

sys.exit(0)
