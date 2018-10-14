import os
import sys

try:  # pragma: no cover (pip>=10)
    from pip._internal import main as pip_main
except ImportError:  # pragma: no cover (pip<10)
    from pip import main as pip_main


def main():
    findlinks, download_dest, pkg, pkgname = sys.argv[1:]
    assert not pip_main(['wheel', pkg, '--wheel-dir', findlinks])
    os.environ.pop('PIP_REQ_TRACKER', None)  # not reentrant
    assert not pip_main([
        'download',
        '--dest', download_dest,
        '--find-links', 'file://{}'.format(findlinks),
        '--no-index',
        pkgname,
    ])
