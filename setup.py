#!/usr/bin/env python

from Cython.Distutils import build_ext
from setuptools import setup, Command, Extension
import os.path


# Directory which libstemmer sources are unpacked in.
library_dir = 'libstemmer_c'


# Directories in libstemmer which contain libstemmer sources (ie, not
# examples, etc).
library_core_dirs = ('src_c', 'runtime', 'libstemmer', 'include')


# Set the include path to include libstemmer.
include_dirs = ('src', os.path.join(library_dir, 'include'))


src_files = ['src/Stemmer.pyx']


class BootstrapCommand(Command):
    description = 'Download libstemmer_c dependency'
    user_options = [
        ('libstemmer-url=', None, 'path to libstemmer c library'),
        ('libstemmer-sha256=', None, 'Expected SHA256 for the tarball'),
    ]

    def initialize_options(self):
        self.libstemmer_url = 'https://snowballstem.org/dist/libstemmer_c.tgz'
        self.libstemmer_sha256 = \
            '054e76f2a05478632f2185025bff0b98952a2b7aed7c4e0960d72ba565de5dfc'

    def finalize_options(self):
        pass

    def run(self):
        from tarballfetcher import download_and_extract_tarball
        download_and_extract_tarball(
            self.libstemmer_url, expected_sha256=self.libstemmer_sha256)


class BuildExtCommand(build_ext):
    def run(self):
        if not os.path.exists(library_dir):
            self.run_command('bootstrap')

        # Read the manifest of files in libstemmer.
        for line in open(os.path.join(library_dir, 'mkinc_utf8.mak')):
            f = line.strip().replace(' \\', '')
            if f.endswith('.c') and os.path.split(f)[0] in library_core_dirs:
                src_files.append(os.path.join(library_dir, f))

        build_ext.run(self)


long_description = r"""

Stemming algorithms

PyStemmer provides access to efficient algorithms for calculating a
"stemmed" form of a word.  This is a form with most of the common
morphological endings removed; hopefully representing a common
linguistic base form.  This is most useful in building search engines
and information retrieval software; for example, a search with stemming
enabled should be able to find a document containing "cycling" given the
query "cycles".

PyStemmer provides algorithms for several (mainly european) languages,
by wrapping the libstemmer library from the Snowball project in a Python
module.

It also provides access to the classic Porter stemming algorithm for
english: although this has been superseded by an improved algorithm, the
original algorithm may be of interest to information retrieval
researchers wishing to reproduce results of earlier experiments.

""".strip()

version_str = '2.0.0'
setup(name='PyStemmer',
      version=version_str,
      author='Richard Boulton',
      author_email='richard@tartarus.org',
      maintainer='Richard Boulton',
      maintainer_email='richard@tartarus.org',
      url='https://github.com/snowballstem/pystemmer/',
      description='Snowball stemming algorithms, for information retrieval',
      long_description=long_description,
      platforms=["any"],
      license="MIT, BSD",
      keywords=[
          "python",
          "information retrieval",
          "language processing",
          "morphological analysis",
          "stemming algorithms",
          "stemmers"
      ],
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "License :: OSI Approved :: BSD License",
          "Natural Language :: Danish",
          "Natural Language :: Dutch",
          "Natural Language :: English",
          "Natural Language :: Finnish",
          "Natural Language :: French",
          "Natural Language :: German",
          "Natural Language :: Italian",
          "Natural Language :: Norwegian",
          "Natural Language :: Portuguese",
          "Natural Language :: Russian",
          "Natural Language :: Spanish",
          "Natural Language :: Swedish",
          "Operating System :: OS Independent",
          "Programming Language :: C",
          "Programming Language :: Other",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Topic :: Database",
          "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
          "Topic :: Text Processing :: Indexing",
          "Topic :: Text Processing :: Linguistic",
      ],
      setup_requires=['Cython>=0.28.5,<1.0'],
      ext_modules=[Extension('Stemmer', src_files,
                             include_dirs=include_dirs)],
      cmdclass={
        'bootstrap': BootstrapCommand,
        'build_ext': BuildExtCommand,
      }
      )
