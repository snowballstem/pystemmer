# Stemmer.pyx: Copyright (c) 2006, Richard Boulton
# Pyrex interface to the snowball "libstemmer_c" library.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

r"""Stemmer: stemming algorithms from the snowball project.

"""
__docformat__ = "restructuredtext en"
# Note: formatted documentation can be retrieved from this file using the
# "epydoc" tool.  Invoke it by compiling this module and then running:
# "epydoc Stemmer.so".

import encodings

cdef extern from "Python.h":
    object PyString_FromStringAndSize (char * s, int len)

cdef extern from "libstemmer.h":
    cdef struct sb_stemmer
    ctypedef unsigned char sb_symbol

    cdef char **      sb_stemmer_list()
    cdef sb_stemmer * sb_stemmer_new(char * algorithm, char * charenc)
    cdef void         sb_stemmer_delete(sb_stemmer * stemmer)
    cdef sb_symbol *  sb_stemmer_stem(sb_stemmer * stemmer, sb_symbol * word, int size)
    cdef int          sb_stemmer_length(sb_stemmer * stemmer)

def algorithms():
    """Get a list of the names of the available stemming algorithms.

    """
    cdef char ** algs
    cdef int i
    py_algs = []
    algs = sb_stemmer_list()
    i = 0
    while algs[i] != NULL:
        py_algs.append(algs[i])
        i = i + 1

    return py_algs

cdef class Stemmer:
    cdef sb_stemmer * cobj
    cdef object cache
    cdef object counter
    cdef int max_cache_size

    def __init__ (self, algorithm, int maxCacheSize = 10000):
        """Initialise a stemmer.

        `algorithm` is the algorithm to use in the new stemmer.

        A list of the valid algorithms may be obtained by calling FIXME.  (Note
        that there are also aliases for these algorithm names, which are not
        included in this list.)

        """
        self.cobj = sb_stemmer_new(algorithm, 'UTF_8')
        if self.cobj == NULL:
            raise KeyError("Stemming algorithm '%s' not found" % algorithm)
        self.max_cache_size = maxCacheSize
        self.counter = 0
        self.cache = {}

    def __dealloc__ (self):
        sb_stemmer_delete(self.cobj)

    property maxCacheSize:
        """Maximum number of entries to allow in the cache.

        This may be set to zero to disable the cache entirely.

        """
        def __set__(self, int size):
            self.max_cache_size = size
            if size == 0:
                self.cache = {}
                self.counter = 0
            else:
                self.__purgeCache()
        def __get__(self):
            return self.max_cache_size

    def __purgeCache (self):
        if len(self.cache) < self.max_cache_size:
            return
        newcache = {}
        mincounter = self.counter - int(self.max_cache_size * 8 / 10)
        for (word, cacheditem) in self.cache.iteritems():
            if cacheditem[1] > mincounter:
                newcache[word] = cacheditem
        self.cache = newcache

    def stemWord (self, word):
        cdef char * c_word
        was_unicode = 0
        if isinstance(word, unicode):
            was_unicode = 1
            word = word.encode('utf-8');

        if self.max_cache_size > 0:
            try:
                cacheditem = self.cache[word]
                result = cacheditem[0]
                cacheditem[1] = self.counter
                self.counter = self.counter + 1
            except KeyError:
                c_word = word
                c_word = <char*>sb_stemmer_stem(self.cobj, <sb_symbol*>c_word, len(word))
                length = sb_stemmer_length(self.cobj)
                result = PyString_FromStringAndSize (c_word, length)
                self.cache[word] = [result, self.counter]
                self.counter = self.counter + 1
                self.__purgeCache()
        else:
            c_word = word
            c_word = <char*>sb_stemmer_stem(self.cobj, <sb_symbol*>c_word, len(word))
            length = sb_stemmer_length(self.cobj)
            result = PyString_FromStringAndSize (c_word, length)

        if was_unicode:
            return result.decode('utf-8')
        return result

    def stemWords (self, words):
        result = []
        for word in words:
            result.append(self.stemWord(word))
        return result
