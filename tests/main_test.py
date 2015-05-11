from __future__ import absolute_import
from __future__ import unicode_literals

import os.path
import subprocess
import sys

import pytest

from testing.util import expected_wheel_name


class CalledProcessError(RuntimeError):
    pass


def call(*cmd):
    proc = subprocess.Popen(
        (
            sys.executable, '-m', 'coverage.__main__', 'run', '-p',
            '-m', 'pip_custom_platform.main',
        ) + cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    if proc.returncode:
        raise CalledProcessError(proc.returncode, out, err)
    return out.decode('utf-8'), err.decode('utf-8')


def wheel(plat, wheeldir, pkg, *args):
    call('wheel', '--platform', plat, '--wheel-dir', wheeldir, pkg, *args)


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
        expected_wheel_name('project_with_c-0.1.0-{0}-{1}-plat.whl'),
    ]


def test_multiple_platforms(tmpdir):
    wheeldir = tmpdir.join('wheelhouse').strpath
    wheel('plat1', wheeldir, 'testing/project_with_c')
    wheel('plat2', wheeldir, 'testing/project_with_c')
    assert set(os.listdir(wheeldir)) == set((
        expected_wheel_name('project_with_c-0.1.0-{0}-{1}-plat1.whl'),
        expected_wheel_name('project_with_c-0.1.0-{0}-{1}-plat2.whl'),
    ))


def test_platform_with_dashes(tmpdir):
    wheeldir = tmpdir.join('wheelhouse').strpath
    wheel('with-dashes', wheeldir, 'testing/project_with_c')
    assert os.listdir(wheeldir) == [
        expected_wheel_name('project_with_c-0.1.0-{0}-{1}-with_dashes.whl'),
    ]


def test_wheel_can_fail(tmpdir):
    with pytest.raises(CalledProcessError):
        wheel('plat1', tmpdir.strpath, 'asdf', '--no-index')


def test_download_smoke(tmpdir):
    findlinks_dir = tmpdir.join('findlinks_dir').strpath
    download_dest = tmpdir.join('downloads')
    download_dest.mkdir()

    # Build a wheel that we'll install
    wheel('plat1', findlinks_dir, 'testing/project_with_c')

    call(
        'install',
        '--platform', 'plat1',
        '--download', download_dest.strpath,
        '--find-links', 'file://{0}'.format(findlinks_dir),
        '--no-index',
        'project_with_c',
    )

    assert os.listdir(download_dest.strpath) == [
        expected_wheel_name('project_with_c-0.1.0-{0}-{1}-plat1.whl'),
    ]


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
        '--find-links', 'file://{0}'.format(findlinks_dir),
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
        '--find-links', 'file://{0}'.format(findlinks_dir),
        '--no-index',
        'project_with_c',
    )

    assert os.listdir(download_dest.strpath) == ['project_with_c-0.1.0.tar.gz']
