from __future__ import absolute_import
from __future__ import unicode_literals

import argparse

from pip_custom_platform.install import install
from pip_custom_platform.wheel import wheel


def add_shared_arguments(parser):
    parser.add_argument(
        '--platform', help='Custom platform name (required).', required=True,
    )
    parser.add_argument(
        'pip_args', nargs='*', help='See pip <command> for other arguments.',
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    install_parser = subparsers.add_parser('install', help='Install packages')
    add_shared_arguments(install_parser)
    install_parser.add_argument(
        '-d', '--download', help='Download packages instead of installing',
    )

    wheel_parser = subparsers.add_parser('wheel', help='Build wheels')
    add_shared_arguments(wheel_parser)
    wheel_parser.add_argument(
        '-w', '--wheel-dir', help='Build wheels into this directory',
        default='./wheelhouse',
    )

    args = parser.parse_args(argv)

    if args.command == 'install':  # pragma: no cover (TODO)
        return install(args.platform, args.pip_args, download=args.download)
    elif args.command == 'wheel':
        return wheel(args.platform, args.wheel_dir, args.pip_args)
    else:
        raise NotImplementedError('{0} not implemented'.format(args.command))


if __name__ == '__main__':
    exit(main())
