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

cdef extern from *:
    ctypedef char** const_char_ptr_ptr "const char **"
    
cdef extern from "Python.h":
    object PyUnicode_FromStringAndSize (char * s, int len)

cdef extern from "libstemmer.h":
    cdef struct sb_stemmer
    ctypedef unsigned char sb_symbol

    cdef const_char_ptr_ptr sb_stemmer_list()
    cdef sb_stemmer * sb_stemmer_new(char * algorithm, char * charenc)
    cdef void         sb_stemmer_delete(sb_stemmer * stemmer)
    cdef sb_symbol *  sb_stemmer_stem(sb_stemmer * stemmer, sb_symbol * word, int size)
    cdef int          sb_stemmer_length(sb_stemmer * stemmer)

def algorithms(aliases=False):
    """Get a list of the names of the available stemming algorithms.
    
    Note that there are also aliases for these algorithm names, which are not
    included in this list by default.  If the 'aliases' keyword parameter is
    False, this list is guaranteed to contain precisely one entry for each
    available stemming algorithm.  Otherwise, all known aliases for algorithms
    will be included in the list.

    Note that the the classic Porter stemming algorithm for English is
    available by default: although this has been superceded by an improved
    algorithm, the original algorithm may be of interest to information
    retrieval researchers wishing to reproduce results of earlier
    experiments.  Most users will want to use the "english" algorithm,
    instead of the "porter" algorithm.

    """
    cdef const_char_ptr_ptr algs
    cdef int i
    py_algs = []
    algs = sb_stemmer_list()
    i = 0
    while algs[i] != NULL:
        alg = algs[i]
        alg = alg.decode(u"ascii")
        py_algs.append(alg)
        i = i + 1
    return py_algs

def version():
    """Get the version string of the stemming module.

    This version number is for the Stemmer module as a whole (not for an
    individual stemming algorithm).

    """
    return '1.2.0'

cdef class Stemmer:
    """An instance of a stemming algorithm.

    The algorithm has internal state, so must not be called concurrently.
    ie, only a single thread should access the instance at any given time.

    When creating a `Stemmer` object, there is one required argument: the
    name of the algorithm to use in the new stemmer.  A list of the valid
    algorithm names may be obtained by calling the `algorithms()` function
    in this module.  In addition, the appropriate stemming algorithm for a
    given language may be obtained by using the 2 or 3 letter ISO 639
    language codes.

    A second optional argument to the constructor for `Stemmer` is the size
    of cache to use.  The cache implemented in this module is not terribly
    efficient, but benchmarks show that it approximately doubles
    performance for typical text processing operations, without too much
    memory overhead.  The cache may be disabled by passing a size of 0.
    The default size (10000 words) is probably appropriate in most
    situations.  In pathological cases (for example, when no word is
    presented to the stemming algorithm more than once, so the cache is
    useless), the cache can severely damage performance.

    The "benchmark.py" script supplied with the PyStemmer distribution can
    be used to test the performance of the stemming algorithms with various
    cache sizes.

    """
    cdef sb_stemmer * cobj
    cdef object cache
    cdef object counter
    cdef int max_cache_size

    def __init__ (self, algorithm, int maxCacheSize = 10000):
        """Initialise a stemmer.

        See the class documentation for details.

        """
        alg = algorithm.encode(u'ascii')
        self.cobj = sb_stemmer_new(alg, 'UTF_8')
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

        The maximum cache size may be set at any point - setting the
        maximum size will purge entries from the cache if the new maximum
        size is smaller than the current size.

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
        """Stem a word.

        This takes a single argument, ``word``, which should either be a UTF-8
        encoded string, or a unicode object.

        The result is the stemmed form of the word.  If the word supplied
        was a unicode object, the result will be a unicode object: if the
        word supplied was a string, the result will be a UTF-8 encoded
        string.

        """
        cdef char * c_word
        was_unicode = 0
        if isinstance(word, unicode):
            was_unicode = 1
            word = word.encode(u'utf-8');

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
                result = PyUnicode_FromStringAndSize (c_word, length)
                self.cache[word] = [result, self.counter]
                self.counter = self.counter + 1
                self.__purgeCache()
        else:
            c_word = word
            c_word = <char*>sb_stemmer_stem(self.cobj, <sb_symbol*>c_word, len(word))
            length = sb_stemmer_length(self.cobj)
            result = PyUnicode_FromStringAndSize (c_word, length)

        if not was_unicode:
            return result.encode(u'utf-8')
        return result

    def stemWords (self, words):
        """Stem a list of words.

        This takes a single argument, ``words``, which must be a sequence,
        iterator, generator or similar.

        The entries in ``words`` should either be UTF-8 encoded strings, or a
        unicode objects.

        The result is a list of the stemmed forms of the words.  If the
        word supplied was a unicode object, the stemmed form will be a
        unicode object: if the word supplied was a string, the stemmed form
        will be a UTF-8 encoded string.

        """
        result = []
        for word in words:
            result.append(self.stemWord(word))
        return result
