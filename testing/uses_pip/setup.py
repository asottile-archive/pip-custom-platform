from setuptools import setup


setup(
    name='uses_pip',
    version='0.1.0',
    py_modules=['uses_pip'],
    entry_points={'console_scripts': ['uses-pip = uses_pip:main']},
)
