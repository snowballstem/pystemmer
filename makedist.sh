#!/bin/sh

python setup.py install --install-lib=`pwd`
epydoc --html -o docs/html Stemmer.so

rm -fr dist
python setup.py sdist
(cd dist &&
 tar zxf PyStemmer*.tar.gz &&
 cd `find -type d|head -n 2|tail -n 1` &&
 python setup.py install --install-lib=`pwd` &&
 python setup.py sdist &&
 python runtests.py
)
