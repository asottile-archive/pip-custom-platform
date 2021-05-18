# DEPRECATED

this is deprecated without replacement.  perhaps encourage pip to implement
[pypa/pip#5453]

[pypa/pip#5453]: https://github.com/pypa/pip/issues/5453

___

[![Build Status](https://dev.azure.com/asottile/asottile/_apis/build/status/asottile.pip-custom-platform?branchName=master)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=60&branchName=master)
[![Azure DevOps coverage](https://img.shields.io/azure-devops/coverage/asottile/asottile/60/master.svg)](https://dev.azure.com/asottile/asottile/_build/latest?definitionId=60&branchName=master)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/asottile/pip-custom-platform/master.svg)](https://results.pre-commit.ci/latest/github/asottile/pip-custom-platform/master)

pip-custom-platform
===================

[pip][pip]+[wheel][wheel] wrapper which allows you to choose a custom platform
name for building, downloading, and installing wheels.

This package assumes you're running your own PyPI server and would like
support for wheels on named platforms that would otherwise be considered
equivalent by the wheel infrastructure (for example not all linux_x86_64 are
created equal).

## Default platform names

By default, pip-custom-platform guesses a platform name for you based on the
`distro` module for Linux, and uses the default platform name on Windows, OS
X, or other systems. Some examples:

| Platform                | Default Platform Name      |
|-------------------------|----------------------------|
| Ubuntu Trusty (14.04)   | linux_ubuntu_14_04_x86_64  |
| Debian Jessie (8)       | linux_debian_8_x86_64      |
| CentOS 7                | linux_centos_7_x86_64      |
| Fedora 22               | linux_fedora_22_x86_64     |
| Red Hat 7               | linux_rhel_7_x86_64        |
| openSUSE 13.2           | linux_opensuse_13_x86_64   |

You can choose your own platform name by passing `--platform my_platform` on
the command line.

## Installation

`pip install pip-custom-platform`

## Usage

### Building wheels

`pip-custom-platform wheel --platform my-platform my-package`

### Downloading distributions

`pip-custom-platform install --platform my-platform --download . my-package`

(or with sufficiently new pip)

`pip-custom-platform download --platform my-platform --dest . my-package`

### Installing packages

`pip-custom-platform install --platform my-platform my-package`


[pip]: https://github.com/pypa/pip
[wheel]: https://bitbucket.org/pypa/wheel
