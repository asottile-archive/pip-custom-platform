from __future__ import absolute_import
from __future__ import unicode_literals

import sys

from distlib.wheel import ABI
from distlib.wheel import IMPVER


def is_py2_or_pypy():
    return str is bytes or '__pypy__' in sys.builtin_module_names


def expected_wheel_name(fmt):
    return fmt.format(IMPVER, 'none' if is_py2_or_pypy() else ABI)
