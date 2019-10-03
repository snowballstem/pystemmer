#!/usr/bin/env python

# This script runs a simple benchmark of the python stemmer interface.

import timeit

datafiles = ('sampledata/englishvoc.txt', 'sampledata/puttydoc.txt',)
words_lst = [None]

for datafile in datafiles:
    words = []
    for line in open(datafile):
        words.extend(line.split())
    for cache_size in (0, 1, 10000, 30000):
        setup = r"""
import Stemmer
stemmer = Stemmer.Stemmer('en', %d)
words = []
for line in open('%s'):
    words.extend(line.split())
""" % (cache_size, datafile)
        t = timeit.Timer(setup=setup,
                         stmt='stemmer.stemWords(words)')
        for iters in (1, 2, 3, 10):
            times = [time / iters for time in t.repeat(5, iters)]
            print "'%s':words=%d,cacheSize=%d,iters=%d,mintime=%f" % \
                (datafile, len(words), cache_size, iters, min(times))
