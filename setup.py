#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand


def make_readme(root_path):
    FILES = ('README.rst', 'TODO', 'CHANGELOG', 'CONTRIBUTORS', 'LICENSE')
    for filename in FILES:
        filepath = os.path.realpath(os.path.join(root_path, filename))
        if os.path.isfile(filepath):
            with open(filepath, mode='r') as f:
                yield f.read()


HERE = os.path.abspath(os.path.dirname(__file__))
LONG_DESCRIPTION = "\r\n\r\n----\r\n\r\n".join(make_readme(HERE))


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ['-vv']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="django-urlbrevity",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'Django>=1.4',
        'hashids>=1.0',
    ],
    tests_require=[
        'coverage>=3.7',
        'pytest>=2.6',
        'pytest-cov>=1.8',
        'pytest-django>=2.7',
    ],
    cmdclass={'test': PyTest},
    author="Keryn Knight",
    author_email='python-package@kerynknight.com',
    description="",
    long_description=LONG_DESCRIPTION,
    keywords="django shortURLs",
    license="BSD License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'License :: OSI Approved :: BSD License',
    ],
    platforms=['OS Independent'],
)
