from __future__ import absolute_import
from __future__ import unicode_literals

from distlib.wheel import ABI
from distlib.wheel import IMPVER


def expected_wheel_name(fmt):
    return fmt.format(IMPVER, 'none' if str is bytes else ABI)
