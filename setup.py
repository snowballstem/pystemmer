#!/usr/bin/env python

from distutils.core import setup, Extension
import os.path

try:
    from Pyrex.Distutils import build_ext
    have_pyrex = 1
except:
    have_pyrex = 0

library_dir = 'libstemmer_c'
library_core_dirs = set(('src_c', 'runtime', 'libstemmer', 'include'))

# Read the manifest of files:
src_files = [os.path.join(library_dir, line.strip())
             for line in open(os.path.join(library_dir, 'MANIFEST'))
             if len(line.strip()) > 2
             and line.strip()[-2:] == '.c'
             and os.path.split(line.strip())[0] in library_core_dirs]

# Set the include path
include_dirs = ('src', os.path.join(library_dir, 'include'))

# Add the pyrex stuff.
if have_pyrex:
    src_files.append('src/Stemmer.pyx')
    cmdclass = {'build_ext': build_ext}
else:
    src_files.append('src/Stemmer.c')
    cmdclass = {}

setup(name = 'PyStemmer',
      version = '0.9',
      description = 'Snowball stemming algorithms',
      author = 'Richard Boulton',
      author_email = 'richard@tartarus.org',

      ext_modules = [Extension('Stemmer', src_files,
                               include_dirs = include_dirs)],
      cmdclass = cmdclass
     )
