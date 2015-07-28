from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib
import os
import platform
import re
import shutil
import tempfile

import distlib.wheel


def default_platform_name():
    """Guess a sane default platform name.

    On OS X and Windows, just uses the default platform name. On Linux, uses
    information from the `platform` module to try to make something reasonable.
    """
    def sanitize(string):
        return re.sub('[^a-z0-9_]', '_', string.lower())

    def grab_version(string, num):
        """Grab the `num` most significant components of a version string.

        >>> grab_version('12.04.1', 2)
        '12.04'
        >>> grab_version('8.2', 1)
        '8'
        """
        return '.'.join(string.split('.')[:num])

    if platform.system() == 'Linux':
        dist, version, __ = platform.linux_distribution()
        dist = re.sub('linux$', '', dist.lower()).strip()

        if dist == 'red hat enterprise linux server':
            dist = 'rhel'

        # Try to determine a good "release" name. This is highly dependent on
        # distribution and what guarantees they provide between versions.
        release = None

        if dist in ['debian', 'rhel', 'centos', 'fedora', 'opensuse']:
            release = grab_version(version, 1)  # one version component
        elif dist in ['ubuntu']:
            release = grab_version(version, 2)  # two version components

        if release:
            return 'linux_{dist}_{release}_{arch}'.format(
                dist=sanitize(dist),
                release=sanitize(release),
                arch=sanitize(platform.machine()),
            )

    # For Windows, OS X, or Linux distributions we couldn't identify, just fall
    # back to whatever pip normally uses.
    return distlib.wheel.ARCH


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
