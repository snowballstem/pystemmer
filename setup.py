#!/usr/bin/env python
from distutils.core import setup, Extension
from distutils.cmd import Command
import os.path
import hashlib
import os
import sys
import tarfile

try:
    from urllib import urlretrieve
    from urlparse import urlparse
except ImportError:
    from urllib.request import urlretrieve
    from urllib.parse import urlparse

try:
    from Cython.Distutils import build_ext

    have_pyrex = 1
except ImportError:
    from distutils.command.build_ext import build_ext

    have_pyrex = 0

# Directory which libstemmer sources are unpacked in.
library_dir = 'libstemmer_c'
src_files = []


class BootstrapCommand(Command):
    description = 'Download libstemmer_c dependency'
    user_options = [
        ('libstemmer-url=', None, 'path to libstemmer c library'),
        ('libstemmer-md5=', None, 'Expected MD5 for the stemmer'),
    ]

    def initialize_options(self):
        self.libstemmer_url = 'http://snowball.tartarus.org/dist/libstemmer_c.tgz'
        self.libstemmer_md5 = '6f32f8f81cd6fa0150333ab540af5e27'

    def finalize_options(self):
        pass

    def download_file(self, url, filename):
        sys.stdout.write('Downloading %s... ' % url)
        sys.stdout.flush()
        urlretrieve(url, filename)
        sys.stdout.write('DONE\n')

    def extract_tarball(self, tarball_filename):
        tarball = tarfile.open(tarball_filename, 'r:gz')
        sys.stdout.write('Extracting %s... ' % tarball_filename)
        sys.stdout.flush()
        tarball.extractall('.')
        sys.stdout.write('DONE\n')

    def md5_file(self, filename):
        return hashlib.md5(open(filename, 'rb').read()).hexdigest()

    def download_and_extract_tarball(self, tarball_url, tarball_filename=None, expected_md5=None):
        if tarball_filename is None:
            tarball_filename = os.path.basename(urlparse(tarball_url).path)

        if not os.path.exists(tarball_filename):
            self.download_file(tarball_url, tarball_filename)

        if not expected_md5 is None:
            sys.stdout.write('Checking that MD5 of %s is %s... ' % (tarball_filename, expected_md5))
            actual_md5 = self.md5_file(tarball_filename)
            sys.stdout.write('MD5 is %s. ' % actual_md5)
            if actual_md5 == expected_md5:
                sys.stdout.write('OK\n')
            else:
                sys.stdout.write('Incorrect MD5!\n')
                sys.exit(1)

        self.extract_tarball(tarball_filename)

    def run(self):
        self.download_and_extract_tarball(
            self.libstemmer_url, expected_md5=self.libstemmer_md5)


class BuildExtCommand(build_ext):
    def run(self):
        if not os.path.exists(library_dir):
            self.run_command('bootstrap')

        # Read the manifest of files in libstemmer.
        src_files.extend([os.path.join(library_dir, line.strip().replace(' \\', ''))
                          for line in open(os.path.join(library_dir, 'mkinc_utf8.mak'))
                          if len(line.strip()) > 2
                          and (line.strip().endswith('.c \\') or line.strip().endswith('.c'))
                          and os.path.split(line.strip().replace(' \\', ''))[0] in library_core_dirs])

        build_ext.run(self)


# Directories in libstemmer which contain libstemmer sources (ie, not
# examples, etc).
library_core_dirs = ('src_c', 'runtime', 'libstemmer', 'include')

# Set the include path to include libstemmer.
include_dirs = ('src', os.path.join(library_dir, 'include'))

cmdclass = {
    'bootstrap': BootstrapCommand,
    'build_ext': BuildExtCommand,
}

if have_pyrex:
    # Add the pyrex sources, and a special rule so distutils knows how to
    # use them.
    src_files.append('src/Stemmer.pyx')
else:
    # Add just the C sources.
    src_files.append('src/Stemmer.c')

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

version_str = '1.3.0'
setup(name = 'PyStemmer',
      version = version_str,
      author = 'Richard Boulton',
      author_email = 'richard@tartarus.org',
      maintainer = 'Richard Boulton',
      maintainer_email = 'richard@tartarus.org',
      url = 'http://snowball.tartarus.org/',
      download_url = 'http://snowball.tartarus.org/wrappers/PyStemmer-%s.tar.gz' % version_str,
      description = 'Snowball stemming algorithms, for information retrieval',
      long_description = long_description,
      platforms = ["any"],
      license = "MIT, BSD",
      keywords = [
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
      "Topic :: Database",
      "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
      "Topic :: Text Processing :: Indexing",
      "Topic :: Text Processing :: Linguistic",
      ],

      ext_modules = [Extension('Stemmer', src_files,
                             include_dirs=include_dirs)],
      cmdclass = cmdclass
      )
