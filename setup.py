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

requires = ["requests>=0.11.1", ]

# This might not be the best idea.
try:
    import json
except ImportError:
    requires.append('simplejson>=2.0')


setup(name='pyspotlight',
      version='0.5.3',
      license='BSD',
      url='https://github.com/newsgrape/pyspotlight',
      packages=find_packages(),
      description='Python interface to the DBPedia Spotlight REST API',
      long_description=open('README.rst').read(),
      keywords="dbpedia spotlight semantic",
      classifiers=classifiers,
      install_requires=requires,
)
