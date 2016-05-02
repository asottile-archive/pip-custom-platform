from __future__ import absolute_import
from __future__ import unicode_literals

from wheel.pep425tags import get_abbr_impl
from wheel.pep425tags import get_abi_tag
from wheel.pep425tags import get_impl_ver


def expected_wheel_name(fmt):
    return fmt.format(get_abbr_impl() + get_impl_ver(), get_abi_tag())
