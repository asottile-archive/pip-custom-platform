from __future__ import absolute_import
from __future__ import unicode_literals

import platform
import re


def _sanitize_platform(platform_name):
    """Platform names must only be alphanumeric with underscores"""
    return re.sub('[^a-z0-9_]', '_', platform_name.lower())


def _default_platform_name(distutils_util_get_platform):
    """Guess a sane default platform name.

    On OS X and Windows, just uses the default platform name. On Linux, uses
    information from the `platform` module to try to make something reasonable.
    """
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
                dist=_sanitize_platform(dist),
                release=_sanitize_platform(release),
                arch=_sanitize_platform(platform.machine()),
            )

    # For Windows, OS X, or Linux distributions we couldn't identify, just fall
    # back to whatever pip normally uses.
    return _sanitize_platform(distutils_util_get_platform())


def get_platform_func(args, distutils_util_get_platform):
    if args.platform:
        platform_name = _sanitize_platform(args.platform)
    else:
        platform_name = _default_platform_name(distutils_util_get_platform)
    return lambda: platform_name
