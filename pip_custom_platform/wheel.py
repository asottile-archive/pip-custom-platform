"""Build packages to a wheel with a custom platform name"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import contextlib
import distutils.util
import os
import shutil
import sys
import tempfile


@contextlib.contextmanager
def tmpdir():
    """Contextmanager to create a temporary directory.  It will be cleaned up
    afterwards.
    """
    tempdir = tempfile.mkdtemp()
    try:
        yield tempdir
    finally:
        shutil.rmtree(tempdir)


def mkdirp(path):
    try:
        os.makedirs(path)
    except OSError:
        if os.path.isdir(path):
            return
        else:
            raise


def _wheel(wheel_dir, pip_main, pip_args):
    mkdirp(wheel_dir)
    # Make the wheels using the platform default
    # Do this in a tempdir in case there are already wheels in the output
    # directory
    with tmpdir() as tempdir:
        ret = pip_main(['wheel', '--wheel-dir', tempdir] + list(pip_args))
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


def get_wheel_main(pip_main, args):
    def main():
        assert sys.argv[1] == 'wheel', sys.argv[1]
        return _wheel(args.wheel_dir, pip_main, sys.argv[2:])
    return main
