#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import python libs
import os
import sys

if 'USE_SETUPTOOLS' in os.environ or 'setuptools' in sys.modules:
    from setuptools import setup
else:
    from distutils.core import setup

NAME = 'pkgcmp'
DESC = ('Automate the creation of a normalized cross distribution package naming database')

# Version info -- read without importing
_locals = {}
with open('pkgcmp/version.py') as fp:
    exec(fp.read(), None, _locals)
VERSION = _locals['__version__']

setup(name=NAME,
      version=VERSION,
      description=DESC,
      author='Thomas S Hatch',
      author_email='thatch@saltstack.com',
      url='https://saltstack.com',
      classifiers=[
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.4',
          ],
      scripts=['scripts/pkgcmp'],
      packages=[
          'pkgcmp',
          'pkgcmp.scanners',
          'pkgcmp.dbs',
          ])
