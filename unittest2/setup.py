#! /usr/bin/env python
# setup.py
# Install script for unittest2
# Copyright (C) 2010 Michael Foord
# E-mail: fuzzyman AT voidspace DOT org DOT uk

# This software is licensed under the terms of the BSD license.
# http://www.voidspace.org.uk/python/license.shtml

import sys
from distutils.core import setup
from unittest2 import __version__ as VERSION

NAME = 'unittest2'

PACKAGES = ['unittest2', 'unittest2.test']
SCRIPTS = ['unit2.py', 'unit2']

DESCRIPTION = 'The new features in unittest for Python 2.7 backported to Python 2.4+.'

URL = 'http://pypi.python.org/pypi/unittest2'

LONG_DESCRIPTION = """
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7. It is tested to run on Python 2.4 - 2.6.

To use unittest2 instead of unittest simply replace ``import unittest`` with
``import unittest2``.

Classes in unittest2 derive from the equivalent classes in unittest, so it
should be possible to use the unittest2 test running infrastructure without
having to switch all your tests to using unittest2 immediately. Similarly
you can use the new assert methods on ``unittest2.TestCase`` with the standard
unittest test running infrastructure. Not all of the new features in unittest2
will work with the standard unittest test loaders and runners however.

New features include:

* ``addCleanups`` - better resource management
* *many* new assert methods including better defaults for comparing lists,
  sets, dicts unicode strings etc and the ability to specify new default methods
  for comparing specific types
* ``assertRaises`` as context manager, with access to the exception afterwards 
* test discovery and new command line options 
* test skipping and expected failures * ``load_tests`` protocol for loading
  tests from modules or packages 
* ``startTestRun`` and ``stopTestRun`` methods on TestResult
* various other API improvements and fixes

.. note::

    In Python 2.7 you invoke the unittest command line features (including test
    discover) with ``python -m unittest <args>``. As unittest is a package, and
    the ability to invoke packages with ``python -m ...`` is new in Python 2.7,
    we can't do this for unittest2.
    
    Instead unittest2 comes with a script ``unit2`. `Command line usage 
    <http://docs.python.org/dev/library/unittest.html#command-line-interface>`_
    ::
    
        unit2 discover
        unit2 -v test_module
    
    There is also a copy of this script called ``unit2.py``, useful for Windows
    which uses file-extensions rather than shebang lines to determine what
    program to execute files with. Both of these scripts are installed by
    distutils.

Until I write proper documentation, the best information on all the new features
is the development version of the Python documentation for Python 2.7:

* http://docs.python.org/dev/library/unittest.html

Look for notes about features added or changed in Python 2.7.

unittest2 is maintained in an SVN repository courtesy of google code:

* http://code.google.com/p/unittest-ext/source/browse/#svn/trunk/unittest2
""".strip()

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.4',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Testing',
]

AUTHOR = 'Michael Foord'

AUTHOR_EMAIL = 'michael@voidspace.org.uk'

KEYWORDS = "unittest testing tests".split(', ')


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
#      download_url=DOWNLOAD_URL,,
      packages=PACKAGES,
      scripts=SCRIPTS,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS
     )
