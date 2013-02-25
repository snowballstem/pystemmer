import os
import sys
import tarfile

try:
    from urllib import urlretrieve
    from urlparse import urlparse
except ImportError:
    from urllib.request import urlretrieve
    from urllib.parse import urlparse

def download_file(url, filename):
    sys.stdout.write('Downloading %s... ' % url)
    sys.stdout.flush()
    urlretrieve(url, filename)
    sys.stdout.write('DONE\n')

def extract_tarball(tarball_filename):
    tarball = tarfile.open(tarball_filename, 'r:gz')
    sys.stdout.write('Extracting %s... ' % tarball_filename)
    sys.stdout.flush()
    tarball.extractall('.')
    sys.stdout.write('DONE\n')

def download_and_extract_tarball(tarball_url, tarball_filename=None):
    if tarball_filename is None:
        tarball_filename = os.path.basename(urlparse(tarball_url).path)

    if not os.path.exists(tarball_filename):
        download_file(tarball_url, tarball_filename)

    extract_tarball(tarball_filename)

