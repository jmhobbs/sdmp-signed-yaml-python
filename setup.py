#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='sdmp-signed-yaml',
      version='0.8',
      description='Implementation of SDMP Signed YAML Specification',
      author='John Hobbs',
      author_email='john@velvetcache.org',
      url='https://github.com/jmhobbs/sdmp-signed-yaml',
      license="MIT",
      packages=['syml'],
      install_requires=['PyYAML', 'pycrypto']
      )
