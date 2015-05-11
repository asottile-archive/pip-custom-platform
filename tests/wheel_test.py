from __future__ import absolute_import

import os

from pip_custom_platform.wheel import wheel
from testing.util import expected_wheel_name


def test_pure_python_package(tmpdir):
    wheeldir = tmpdir.join('wheelhouse')
    wheel('custom_plat', wheeldir.strpath, ('testing/pure_py_project',))
    assert os.listdir(wheeldir.strpath) == [
        'pure_python_project-0.1.0-py2.py3-none-any.whl',
    ]


def test_project_with_c(tmpdir):
    wheeldir = tmpdir.join('wheelhouse')
    wheel('custom_plat', wheeldir.strpath, ('testing/project_with_c',))
    assert os.listdir(wheeldir.strpath) == [
        expected_wheel_name('project_with_c-0.1.0-{0}-{1}-custom_plat.whl'),
    ]


def test_multiple_platforms(tmpdir):
    wheeldir = tmpdir.join('wheelhouse')
    wheel('plat1', wheeldir.strpath, ('testing/project_with_c',))
    wheel('plat2', wheeldir.strpath, ('testing/project_with_c',))
    assert set(os.listdir(wheeldir.strpath)) == set((
        expected_wheel_name('project_with_c-0.1.0-{0}-{1}-plat1.whl'),
        expected_wheel_name('project_with_c-0.1.0-{0}-{1}-plat2.whl'),
    ))
