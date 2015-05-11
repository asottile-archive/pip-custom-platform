# pylint:disable=import-error,no-member,no-name-in-module
from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib
import distutils.util


@contextlib.contextmanager
def patch_platform_name(platform_name):
    """The gross part: monkeypatching."""
    original_get_platform = distutils.util.get_platform
    distutils.util.get_platform = lambda: platform_name
    try:
        yield
    finally:
        distutils.util.get_platform = original_get_platform


def install(platform_name, pip_args):
    with patch_platform_name(platform_name):
        import pip
        return pip.main(['install'] + list(pip_args))
