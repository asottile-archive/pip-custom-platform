from __future__ import absolute_import
from __future__ import unicode_literals

import contextlib
import os

from distlib.wheel import ABI
from distlib.wheel import IMPVER


@contextlib.contextmanager
def cwd(path):
    original_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(original_cwd)


def expected_wheel_name(fmt):
    return fmt.format(IMPVER, 'none' if str is bytes else ABI)
