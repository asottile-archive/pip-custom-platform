"""Build packages to a wheel with a custom platform name"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import contextlib
import distutils.util
import os
import shutil
import sys
import tempfile


@contextlib.contextmanager
def tmpdir():
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


def _wheel(wheel_dir, pip_main, pip_args):
    mkdirp(wheel_dir)
    # Wheels will always be build with the default platform (due to pip
    # subprocessing to build the wheel).
    # Do this in a tempdir in case there are already wheels in the output
    # directory
    with tmpdir() as tempdir:
        ret = pip_main(['wheel', '--wheel-dir', tempdir] + pip_args)
        if ret:
            return ret

        # Then rename any of the platform-specific wheels created
        for wheel_filename in os.listdir(tempdir):
            if not wheel_filename.endswith('-any.whl'):
                before, _ = wheel_filename.rsplit('-', 1)
                new_wheel_filename = '{}-{}.whl'.format(
                    before, distutils.util.get_platform(),
                )
            else:
                new_wheel_filename = wheel_filename
            dst = os.path.join(wheel_dir, new_wheel_filename)

            # And copy to the output directory
            shutil.copy(os.path.join(tempdir, wheel_filename), dst)


def _show_platform_name():
    print(distutils.util.get_platform())
    return 0


def get_main(pip_main):
    def main(argv=None):
        argv = argv if argv is not None else sys.argv[1:]

        def _add_platform_param(parser):
            parser.add_argument(
                '--platform', help=(
                    'Custom platform name.  The default is auto-detected -- '
                    'Use `pip-custom-platform show-platform-name` to show.'
                ),
            )

        parser = argparse.ArgumentParser(
            prog='pip-custom-platform',
            description=(
                'pip+wheel wrapper which allows you to choose a custom '
                'platform name for building, downloading, and installing '
                'wheels.\n\n'
                'Any unparsed command arguments will be passed on to pip\n'
            ),
        )
        subparsers = parser.add_subparsers(dest='command')
        subparsers.required = True

        install = subparsers.add_parser('install', help='Install packages')
        _add_platform_param(install)

        download = subparsers.add_parser('download', help='Download packages')
        _add_platform_param(download)

        platform_name = subparsers.add_parser(
            'show-platform-name', help='Show the default platform name',
        )
        _add_platform_param(platform_name)

        wheel = subparsers.add_parser('wheel', help='Build wheels')
        _add_platform_param(wheel)
        wheel.add_argument(
            '-w', '--wheel-dir', help='Build wheels into this directory',
            default='./wheelhouse',
        )

        args, rest = parser.parse_known_args(argv)
        if args.command in ('install', 'download'):
            return pip_main([args.command] + rest)
        elif args.command == 'wheel':
            return _wheel(args.wheel_dir, pip_main, rest)
        elif args.command == 'show-platform-name':
            return _show_platform_name()
        else:
            raise NotImplementedError(args.command)
    return main
