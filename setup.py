#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from setuptools import find_packages


classifiers = [
    "Intended Audience :: Developers",
    "Programming Language :: Python",
    "Operating System :: OS Independent",
    "Topic :: Software Development :: Libraries",
    "Environment :: Web Environment",
    "License :: OSI Approved :: BSD License",
    "Development Status :: 5 - Production/Stable",
]

requires = ["requests>=2.6.0", ]

# This might not be the best idea.
try:
    import json
except ImportError:
    requires.append('simplejson>=2.0')


# Python 2.6 does not ship with an OrderedDict implementation.
# God save the cheeseshop!
try:
    from collections import OrderedDict
except ImportError:
    requires.append('ordereddict>=1.1')


setup(name='pyspotlight',
      version='0.6.5.2',
      license='BSD',
      url='https://github.com/newsgrape/pyspotlight',
      packages=find_packages(),
      description='Python interface to the DBPedia Spotlight REST API',
      long_description=open('README.rst').read(),
      keywords="dbpedia spotlight semantic",
      classifiers=classifiers,
      install_requires=requires,
)
