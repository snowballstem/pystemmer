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


def sha256_file(filename):
    return hashlib.sha256(open(filename, 'rb').read()).hexdigest()


def download_and_extract_tarball(tarball_url,
                                 tarball_filename=None,
                                 expected_sha256=None):
    if tarball_filename is None:
        tarball_filename = os.path.basename(urlparse(tarball_url).path)

    if not os.path.exists(tarball_filename):
        download_file(tarball_url, tarball_filename)

    if expected_sha256 is not None:
        sys.stdout.write('Checking that SHA256 of %s is %s... ' %
                         (tarball_filename, expected_sha256))
        actual_sha256 = sha256_file(tarball_filename)
        sys.stdout.write('SHA256 is %s. ' % actual_sha256)
        if actual_sha256 == expected_sha256:
            sys.stdout.write('OK\n')
        else:
            sys.stdout.write('Incorrect SHA256!\n')
            sys.exit(1)

    extract_tarball(tarball_filename)
