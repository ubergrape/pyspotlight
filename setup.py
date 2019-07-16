#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
from setuptools import find_packages
from io import open


classifiers = [
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Environment :: Web Environment',
    'License :: OSI Approved :: BSD License',
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

requires = [
    'requests~=2.10',
]
tests_require = [
    'nose2~=0.6',
]

with open('README.rst', 'r', encoding='utf-8') as f:
    readme = f.read()
with open('HISTORY.rst', 'r', encoding='utf-8') as f:
    history = f.read()


setup(name='pyspotlight',
      version='0.7.2',
      license='BSD',
      url='https://github.com/aolieman/pyspotlight',
      author='Luis Nell',
      author_email='luis.nell@simpleloop.com',
      maintainer='Alex Olieman',
      maintainer_email='alex@olieman.net',
      packages=find_packages(),
      description='Python interface to the DBpedia Spotlight REST API',
      long_description=readme + '\n\n' + history,
      keywords=['dbpedia spotlight', 'semantic annotation', 'entity linking'],
      classifiers=classifiers,
      install_requires=requires,
      tests_require=tests_require,
      test_suite='nose2.collector.collector',
)
