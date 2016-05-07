from __future__ import print_function
from __future__ import unicode_literals

import collections
import distutils.util
import functools
import os.path
import subprocess

import mock
import pytest

from pip_custom_platform.default_platform import _default_platform_name
from pip_custom_platform.default_platform import _sanitize_platform


default_platform_name = functools.partial(
    _default_platform_name, distutils.util.get_platform,
)


SETUP_DEBIAN = (
    'apt-get update -qq',
    'DEBIAN_FRONTEND=noninteractive apt-get install -qq -y ' +
    '    --no-install-recommends python python-pip >&2'
)
SETUP_NO_PIP_PACKAGE = (
    # for systems with no pip system package (or RHEL which wants $$$$)
    'curl "https://bootstrap.pypa.io/get-pip.py" | python >&2',
)

SystemTestCase = collections.namedtuple('SystemTestCase', (
    'docker_image',
    'mock_linux_dist',
    'expected_platform_name',
    'setup_script',
))

SYSTEM_TESTCASES = [
    SystemTestCase(
        docker_image='ubuntu:trusty',
        mock_linux_dist=('Ubuntu', '14.04', 'trusty'),
        expected_platform_name='linux_ubuntu_14_04_x86_64',
        setup_script=SETUP_DEBIAN,
    ),
    SystemTestCase(
        docker_image='debian:jessie',
        mock_linux_dist=('debian', '8.1', ''),
        expected_platform_name='linux_debian_8_x86_64',
        setup_script=SETUP_DEBIAN,
    ),
    SystemTestCase(
        docker_image='centos:centos7',
        mock_linux_dist=('CentOS Linux', '7.1.1503', 'Core'),
        expected_platform_name='linux_centos_7_x86_64',
        setup_script=SETUP_NO_PIP_PACKAGE,
    ),
    SystemTestCase(
        docker_image='fedora:22',
        mock_linux_dist=('Fedora', '22', 'Twenty Two'),
        expected_platform_name='linux_fedora_22_x86_64',
        setup_script=('yum install -y python-pip >&2',),
    ),
    SystemTestCase(
        docker_image='rhel7',
        mock_linux_dist=('Red Hat Enterprise Linux Server', '7.1', 'Maipo'),
        expected_platform_name='linux_rhel_7_x86_64',
        setup_script=SETUP_NO_PIP_PACKAGE,
    ),
    SystemTestCase(
        docker_image='opensuse:13.2',
        mock_linux_dist=('openSUSE ', '13.2', 'x86_64'),
        expected_platform_name='linux_opensuse_13_x86_64',
        setup_script=(
            'zypper --non-interactive install python python-pip >&2',
        )
    ),
    SystemTestCase(
        docker_image='base/archlinux',
        mock_linux_dist=('arch', '', ''),
        expected_platform_name='linux_x86_64',
        setup_script=(
            'pacman -Syy >&2',
            'pacman -S --noconfirm python python-pip >&2',
        )
    ),
]


@pytest.mark.parametrize('case', SYSTEM_TESTCASES)
@mock.patch('pip_custom_platform.default_platform.platform')
def test_platform_linux(mock_platform, case):
    mock_platform.system.return_value = 'Linux'
    mock_platform.machine.return_value = 'x86_64'
    mock_platform.linux_distribution.return_value = case.mock_linux_dist
    assert default_platform_name() == case.expected_platform_name


@mock.patch('pip_custom_platform.default_platform.platform')
def test_platform_notlinux(mock_platform):
    mock_platform.system.return_value = "it's a unix system!"
    ret = default_platform_name()
    assert ret == _sanitize_platform(distutils.util.get_platform())


PLATFORM_SCRIPT = '''\
from distutils.util import get_platform
from pip_custom_platform.default_platform import _default_platform_name
print(_default_platform_name(get_platform))
'''


@pytest.mark.skipif(
    'not config.getvalue("docker")',
    reason="Requires --docker",
)
class TestDistributionNameDockerIntegration(object):  # pragma: no cover
    """Launch Docker containers to test platform strings.

    These tests are slow and take up a lot of disk space. They are only run if
    `--docker` is passed to pytest on the command line.
    """
    # pylint: disable=no-self-use

    @pytest.mark.parametrize('case', SYSTEM_TESTCASES)
    def test_platform_name(self, case):
        """Ensure the default_platform_name() output matches what we expect."""
        commands = case.setup_script + (
            'pip install /mnt >&2',
            'python -c "{}"'.format(PLATFORM_SCRIPT)
        )
        stdout = run_in_docker(case.docker_image, commands)
        assert stdout.strip() == case.expected_platform_name

    @pytest.mark.parametrize('case', SYSTEM_TESTCASES)
    def test_mock_is_accurate(self, case):
        """Ensure our mocks for platform.linux_distribution() are accurate."""
        commands = case.setup_script + (
            'python -c "import platform\nprint(platform.linux_distribution())"',  # noqa
        )
        stdout = run_in_docker(case.docker_image, commands)
        assert stdout.strip() == str(case.mock_linux_dist)


def run_in_docker(image, commands):  # pragma: no cover
    """Launches the Docker image and executes the commands, returning
    stdout and stderr.

    :param image: a Docker image and tag (e.g. 'debian:jessie')
    :param commands: list of commands to paste to the shell
    """
    repo_dir = os.path.abspath(os.path.join(__file__, '../../'))
    mount_option = '{}:/mnt:ro'.format(repo_dir)

    cmd = ('docker', 'run', '-v', mount_option, '-i', image, 'sh')
    proc = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    )

    lines = '\n'.join(commands)
    return proc.communicate(lines.encode('utf-8'))[0].decode('utf-8')
