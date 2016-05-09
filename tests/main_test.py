from __future__ import absolute_import
from __future__ import unicode_literals

import os.path
import subprocess
import sys

import mock
import pytest

from testing.util import expected_wheel_name


def call(*cmd):
    subprocess.check_call(
        (
            sys.executable, '-m', 'coverage.__main__', 'run', '-p',
            '-m', 'pip_custom_platform.main',
        ) + cmd,
    )


def wheel(plat, wheeldir, pkg, *args):
    call('wheel', '--platform', plat, '--wheel-dir', wheeldir, pkg, *args)


def test_useful_message_with_no_args(capfd):
    """We should print a useful message when called with no arguments."""
    with pytest.raises(subprocess.CalledProcessError):
        call()
    _, err = capfd.readouterr()
    assert 'usage: main.py' in err


def test_pure_python_package(tmpdir):
    wheeldir = tmpdir.join('wheelhouse').strpath
    wheel('plat', wheeldir, 'testing/pure_py_project')
    assert os.listdir(wheeldir) == [
        'pure_python_project-0.1.0-py2.py3-none-any.whl',
    ]


def test_project_with_c(tmpdir):
    wheeldir = tmpdir.join('wheelhouse').strpath
    wheel('plat', wheeldir, 'testing/project_with_c')
    assert os.listdir(wheeldir) == [
        expected_wheel_name('project_with_c-0.1.0-{}-{}-plat.whl'),
    ]


def test_multiple_platforms(tmpdir):
    wheeldir = tmpdir.join('wheelhouse').strpath
    wheel('plat1', wheeldir, 'testing/project_with_c')
    wheel('plat2', wheeldir, 'testing/project_with_c')
    assert set(os.listdir(wheeldir)) == {
        expected_wheel_name('project_with_c-0.1.0-{}-{}-plat1.whl'),
        expected_wheel_name('project_with_c-0.1.0-{}-{}-plat2.whl'),
    }


def test_platform_with_dashes(tmpdir):
    wheeldir = tmpdir.join('wheelhouse').strpath
    wheel('with-dashes', wheeldir, 'testing/project_with_c')
    assert os.listdir(wheeldir) == [
        expected_wheel_name('project_with_c-0.1.0-{}-{}-with_dashes.whl'),
    ]


def test_wheel_can_fail(tmpdir):
    with pytest.raises(subprocess.CalledProcessError):
        wheel('plat1', tmpdir.strpath, 'asdf', '--no-index')


def test_download_smoke(tmpdir):
    findlinks_dir = tmpdir.join('findlinks_dir').strpath
    download_dest = tmpdir.join('downloads').mkdir().strpath

    # Build a wheel that we'll install
    wheel('plat1', findlinks_dir, 'testing/project_with_c')

    call(
        'install',
        '--platform', 'plat1',
        '--download', download_dest,
        '--find-links', 'file://{}'.format(findlinks_dir),
        '--no-index',
        'project_with_c',
    )

    assert os.listdir(download_dest) == [
        expected_wheel_name('project_with_c-0.1.0-{}-{}-plat1.whl'),
    ]


def test_default_platform(tmpdir):
    findlinks_dir = tmpdir.join('findlinks_dir').strpath
    download_dest = tmpdir.join('downloads').mkdir().strpath

    call('wheel', '--wheel-dir', findlinks_dir, 'testing/project_with_c')

    call(
        'install',
        '--download', download_dest,
        '--find-links', 'file://{}'.format(findlinks_dir),
        '--no-index',
        'project_with_c',
    )

    # We don't _really_ know what the default platform is on this system, so
    # just assert that we get something
    assert os.listdir(download_dest)


def test_download_falls_back_to_sdist(tmpdir):
    findlinks_dir = tmpdir.join('findlinks_dir').strpath
    download_dest = tmpdir.join('downloads')
    download_dest.mkdir()

    # Build an sdist
    subprocess.check_call(
        (
            sys.executable, 'setup.py', 'sdist',
            '--dist-dir', findlinks_dir,
        ),
        cwd='testing/project_with_c',
    )

    call(
        'install',
        '--platform', 'plat1',
        '--download', download_dest.strpath,
        '--find-links', 'file://{}'.format(findlinks_dir),
        '--no-index',
        'project_with_c',
    )

    assert os.listdir(download_dest.strpath) == ['project_with_c-0.1.0.tar.gz']


def test_download_wrong_plat_falls_back_to_sdist(tmpdir):
    findlinks_dir = tmpdir.join('findlinks_dir').strpath
    download_dest = tmpdir.join('downloads')
    download_dest.mkdir()

    # Build an sdist
    subprocess.check_call(
        (
            sys.executable, 'setup.py', 'sdist',
            '--dist-dir', findlinks_dir,
        ),
        cwd='testing/project_with_c',
    )

    # Also build a wheel
    wheel('plat2', findlinks_dir, 'testing/project_with_c')

    call(
        'install',
        '--platform', 'plat1',
        '--download', download_dest.strpath,
        '--find-links', 'file://{}'.format(findlinks_dir),
        '--no-index',
        'project_with_c',
    )

    assert os.listdir(download_dest.strpath) == ['project_with_c-0.1.0.tar.gz']


def test_show_platform_name_custom_platform(capfd):
    call('show-platform-name', '--platform', 'herp-derp')
    assert capfd.readouterr() == ('herp_derp\n', '')


def test_show_platform_name_default(capfd):
    call('show-platform-name')
    assert capfd.readouterr() == (mock.ANY, '')
