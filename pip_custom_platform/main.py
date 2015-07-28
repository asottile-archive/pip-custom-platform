from __future__ import absolute_import
from __future__ import unicode_literals

import argparse

from pip_custom_platform.install import install
from pip_custom_platform.util import default_platform_name
from pip_custom_platform.wheel import wheel


def add_shared_arguments(parser):
    default_platform = default_platform_name()
    parser.add_argument(
        '--platform',
        default=default_platform,
        help='Custom platform name (default: {0})'.format(default_platform),
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            'pip+wheel wrapper which allows you to choose a custom platform '
            'name for building, downloading, and installing wheels.\n\n'
            'Any unparsed command arguments will be passed on to pip\n'
        ),
    )
    subparsers = parser.add_subparsers(dest='command')

    install_parser = subparsers.add_parser('install', help='Install packages')
    add_shared_arguments(install_parser)

    wheel_parser = subparsers.add_parser('wheel', help='Build wheels')
    add_shared_arguments(wheel_parser)
    wheel_parser.add_argument(
        '-w', '--wheel-dir', help='Build wheels into this directory',
        default='./wheelhouse',
    )

    args, argv = parser.parse_known_args(argv)

    platform = args.platform.replace('-', '_')

    if args.command == 'install':
        return install(platform, argv)
    elif args.command == 'wheel':
        return wheel(platform, args.wheel_dir, argv)
    else:
        raise NotImplementedError('{0} not implemented'.format(args.command))


if __name__ == '__main__':
    exit(main())
