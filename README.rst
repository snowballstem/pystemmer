PyStemmer
=========

What is PyStemmer?
------------------

PyStemmer is a Python interface to the stemming algorithms from the Snowball
project (http://snowball.tartarus.org/). A stemming algorithm (or stemmer) is a
process for removing the commoner morphological and inflexional endings from
words in English. Its main use is as part of a term normalisation process that
is usually done when setting up Information Retrieval systems.  A stemmer aims
to conflate words with the same linguistic base form, in order that the
resulting "stem" may be considered to represent all words with that base form.

Stemmers can be used to make searches more comprehensive. For example, stemming
can ensure that a search for 'cars' will also find all documents that contain
only 'car'.

Snowball is a small string processing language designed for creating stemming
algorithms for use in Information Retrieval.  It is also the name of a project
to develop a good base set of stemming algorithms.

PyStemmer uses the "libstemmer_c" C interface to the snowball algorithms,
provided by the snowball project itself.  This library is unmodified, but
contained within the PyStemmer distribution.  If you wish to upgrade PyStemmer
to a more recent version of libstemmer_c (or the snowball algorithms), it
should suffice to download a new copy of libstemmer_c from the snowball
project, and replace the contents of the libstemmer_c subdirectory with the
contents of the download.

Requirements
------------

This version of PyStemmer has been tested using Python series 2.6, 2.7, 3.3,
3.4, 3.5, 3.6 and pypy.  Builds are checked with `travis`_:

.. _travis: https://travis-ci.org/snowballstem/pystemmer

.. image:: https://travis-ci.org/snowballstem/pystemmer.png?branch=master
   :target: https://travis-ci.org/snowballstem/pystemmer

Installation
------------

To build PyStemmer from a source code checkout (i.e.: Subversion or Git), you
will need to download a copy of libstemmer_c and unpack it -- e.g.:

    curl -s http://snowball.tartarus.org/dist/libstemmer_c.tgz | tar xzf -

The above step is unncessary if you've downloaded a source distribution of
PyStemmer (i.e.: a .tar.gz or .zip file).

PyStemmer uses distutils, so all that is necessary to build and install
PyStemmer is the usual distutils invocation:

    python setup.py install

API
---

PyStemmer's API is documented by documentation comments, which may conveniently
be viewed using the epydoc output present in the docs/html/ subdirectory.

A brief overview can be found in docs/quickstart.txt

License
-------

PyStemmer is copyright (c) 2006, Richard Boulton, and is licensed under the MIT
license: see the file "LICENSE" for the full text of this.  It is was inspired
by an earlier implementation (which was copyright (c) 2001, Andreas Jung, and
also licensed under the MIT license, but no portions of which remain in this
package, and had a different API).

The snowball algorithms, and the snowball library, are copyright (c) 2001-2006,
Dr Martin Porter and Richard Boulton, and are licensed under the BSD license.
