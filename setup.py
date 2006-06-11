#!/usr/bin/env python

from distutils.core import setup, Extension
import os.path

try:
    from Pyrex.Distutils import build_ext
    have_pyrex = 1
except:
    have_pyrex = 0

# Directory which libstemmer sources are unpacked in.
library_dir = 'libstemmer_c'
# Directories in libstemmer which contain libstemmer sources (ie, not
# examples, etc).
library_core_dirs = set(('src_c', 'runtime', 'libstemmer', 'include'))

# Read the manifest of files in libstemmer.
src_files = [os.path.join(library_dir, line.strip())
             for line in open(os.path.join(library_dir, 'MANIFEST'))
             if len(line.strip()) > 2
             and line.strip()[-2:] == '.c'
             and os.path.split(line.strip())[0] in library_core_dirs]
# Set the include path to include libstemmer.
include_dirs = ('src', os.path.join(library_dir, 'include'))

if have_pyrex:
    # Add the pyrex sources, and a special rule so distutils knows how to
    # use them.
    src_files.append('src/Stemmer.pyx')
    cmdclass = {'build_ext': build_ext}
else:
    # Add just the C sources.
    src_files.append('src/Stemmer.c')
    cmdclass = {}

setup(name = 'PyStemmer',
      version = '0.9',
      author = 'Richard Boulton',
      author_email = 'richard@tartarus.org',
      maintainer = 'Richard Boulton',
      maintainer_email = 'richard@tartarus.org',
      url = 'http://snowball.tartarus.org/',
      description = 'Snowball stemming algorithms, for information retrieval',
      long_description = """
      PyStemmer provides access to efficient algorithms for calculating a
      "stemmed" form of a word.  This is a form with most of the common
      morphological endings removed; hopefully representing a common linguistic
      base form.  This is most useful in building search engines and
      information retrieval software; for example, a search with stemming
      enabled should be able to find a document containing "cycling" given the
      query "cycles".
      
      PyStemmer provides algorithms for several (mainly european) languages,
      by wrapping the libstemmer library from the Snowball project in a
      Python module.
      """

      ext_modules = [Extension('Stemmer', src_files,
                               include_dirs = include_dirs)],
      cmdclass = cmdclass
     )
