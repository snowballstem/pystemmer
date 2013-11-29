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

def md5_file(filename):
    return hashlib.md5(open(filename, 'rb').read()).hexdigest()

def download_and_extract_tarball(tarball_url, tarball_filename=None, expected_md5=None):
    if tarball_filename is None:
        tarball_filename = os.path.basename(urlparse(tarball_url).path)

    if not os.path.exists(tarball_filename):
        download_file(tarball_url, tarball_filename)

    if not expected_md5 is None:
        sys.stdout.write('Checking that MD5 of %s is %s... ' % (tarball_filename, expected_md5))
        actual_md5 = md5_file(tarball_filename)
        sys.stdout.write('MD5 is %s. ' % actual_md5)
        if actual_md5 == expected_md5:
            sys.stdout.write('OK\n')
        else:
            sys.stdout.write('Incorrect MD5!\n')
            sys.exit(1)

    extract_tarball(tarball_filename)

