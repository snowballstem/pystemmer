#!/usr/bin/env python

from distutils.core import setup, Extension
import os.path

library_dir = 'libstemmer_c'
library_core_dirs = set(('src_c', 'runtime', 'libstemmer', 'include'))

# Read the manifest of files:
src_files = [os.path.join(library_dir, line.strip())
             for line in open(os.path.join(library_dir, 'MANIFEST'))
             if len(line.strip()) > 2
             and line.strip()[-2:] == '.c'
             and os.path.split(line.strip())[0] in library_core_dirs]
src_files.append('src/Stemmer.c')
include_dirs = ('src', os.path.join(library_dir, 'include'))

setup(name = 'PyStemmer',
      version = '0.9',
      description = 'Snowball stemming algorithms',
      author = 'Richard Boulton',
      author_email = 'richard@tartarus.org',

      ext_modules = [Extension('Stemmer', src_files,
                               include_dirs = include_dirs)]
     )
