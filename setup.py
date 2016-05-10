from setuptools import find_packages
from setuptools import setup

setup(
    name='pip_custom_platform',
    description=(
        'pip + wheel wrapper which allows you to choose a custom platform '
        'name for building, downloading, and installing wheels.'
    ),
    url='https://github.com/asottile/pip-custom-platform',
    version='0.3.0',
    author='Anthony Sottile',
    author_email='asottile@umich.edu',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages(exclude=('tests*', 'testing*')),
    install_requires=['pip', 'wheel', 'pymonkey>=0.2.0'],
    entry_points={
        'console_scripts': [
            'pip-custom-platform = pip_custom_platform.main:main',
        ],
        'pymonkey': ['pip-custom-platform = pip_custom_platform.pymonkey'],
        'pymonkey.argparse': [
            'pip-custom-platform = pip_custom_platform.pymonkey',
        ],
    },
)
