import sys

import pip


def main():
    findlinks, download_dest, pkg, pkgname = sys.argv[1:]
    assert not pip.main(['wheel', pkg, '--wheel-dir', findlinks])
    assert not pip.main([
        'install',
        '--download', download_dest,
        '--find-links', 'file://{}'.format(findlinks),
        '--no-index',
        pkgname,
    ])
