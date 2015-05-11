"""Build packages to a wheel with a custom platform name"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil

from distlib.wheel import Wheel

from pip_custom_platform.util import mkdirp
from pip_custom_platform.util import tmpdir


def wheel(platform_name, wheel_dir, pip_args):
    mkdirp(wheel_dir)
    # Make the wheels using the platform default
    # Do this in a tempdir in case there are already wheels in the output
    # directory
    with tmpdir() as tempdir:
        import pip
        ret = pip.main(['wheel', '--wheel-dir', tempdir] + list(pip_args))
        if ret:
            return ret

        # Then rename any of the platform-specific wheels created
        for wheel_filename in os.listdir(tempdir):
            wheel_obj = Wheel(wheel_filename)

            if wheel_obj.arch != ['any']:
                wheel_obj.arch = [platform_name]
                dst = os.path.join(wheel_dir, wheel_obj.filename)
            else:
                dst = os.path.join(wheel_dir, wheel_filename)

            # And copy to the output directory
            shutil.copy(os.path.join(tempdir, wheel_filename), dst)
