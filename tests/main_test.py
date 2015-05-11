from __future__ import absolute_import
from __future__ import unicode_literals

import os.path

from pip_custom_platform.main import main
from testing.util import cwd
from testing.util import expected_wheel_name


def test_wheel_smoke(tmpdir):
    c_package_path = os.path.abspath('testing/project_with_c')
    with cwd(tmpdir.strpath):
        main(('wheel', '--platform', 'plat1', c_package_path))
        assert os.path.exists(
            'wheelhouse/{0}'.format(
                expected_wheel_name('project_with_c-0.1.0-{0}-{1}-plat1.whl'),
            ),
        )
