[![Build Status](https://travis-ci.org/asottile/pip-custom-platform.svg?branch=master)](https://travis-ci.org/asottile/pip-custom-platform)
[![Coverage Status](https://img.shields.io/coveralls/asottile/pip-custom-platform.svg?branch=master)](https://coveralls.io/r/asottile/pip-custom-platform)

pip-custom-platform
===================

pip+wheel wrapper which allows you to choose a custom platform name for
building, downloading, and installing wheels.

This package assumes you're running your own pypi server and would like
support for wheels on named platforms what would otherwise be considered
equivalent by the wheel infrastructure (for example not all linux_x86_64 are
created equal).

pip: https://github.com/pypa/pip

wheel: https://bitbucket.org/pypa/wheel

## Installation

`pip install pip-custom-platform`

## Usage

### Building wheels

`pip-custom-platform wheel --platform my-platform my-package`

### Downloading distributions

`pip-custom-platform install --platform my-platform --download . my-package`

### Installing packages

`pip-custom-platform install --platform my-platform my-package`
