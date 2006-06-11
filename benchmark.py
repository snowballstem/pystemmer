#!/usr/bin/env python

import timeit

for cache_size in (0, 1, 10000, 30000):
    setup = r"""
import Stemmer
stemmer = Stemmer.Stemmer('en', %d)
fd = open('../data/english/voc.txt')
words = fd.readlines()
""" % cache_size
    t = timeit.Timer(setup=setup,
                     stmt='stemmer.stemWords(words)')
    for iters in (1, 2, 3, 10):
        times = [time / iters for time in t.repeat(5, iters)]
        print "cacheSize=%d,iters=%d,time=%f" % (cache_size, iters, min(times))
