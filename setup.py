#!/usr/bin/env python
# setup.py
# Install script for discover.py
# Copyright (C) 2009-2010 Michael Foord
# E-mail: michael AT voidspace DOT org DOT uk

# This software is licensed under the terms of the BSD license.
# http://www.voidspace.org.uk/python/license.shtml

import sys
from distutils.core import setup
from discover import __version__ as VERSION

from distutils.core import setup

NAME = 'discover'
MODULES = ('discover',)
DESCRIPTION = 'Test discovery for unittest. Backported from Python 2.7 for Python 2.4+'
URL = 'http://pypi.python.org/pypi/discover/'
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.4',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.0',
    'Programming Language :: Python :: 3.1',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
]
AUTHOR = 'Michael Foord'
AUTHOR_EMAIL = 'michael@voidspace.org.uk'
KEYWORDS = "unittest, testing, tests".split(', ')
LONG_DESCRIPTION = """
This is the test discovery mechanism and ``load_tests`` protocol for unittest
backported from Python 2.7 to work with Python 2.4 or more recent (including 
Python 3).

discover can be installed with pip or easy_install. After installing switch the
current directory to the top level directory of your project and run::

   python -m discover
   python discover.py

This will discover all tests (with certain restrictions) from the current
directory. The discover module has several options to control its behavior (full
usage options are displayed with ``python -m discover -h``)::

    Usage: discover.py [options]

    Options:
      -v, --verbose    Verbose output
      -s directory     Directory to start discovery ('.' default)
      -p pattern       Pattern to match test files ('test*.py' default)
      -t directory     Top level directory of project (default to
                       start directory)

    For test discovery all test modules must be importable from the top
    level directory of the project.

For example to use a different pattern for matching test modules run::

    python -m discover -p '*test.py'

(Remember to put quotes around the test pattern or shells like bash will do
shell expansion rather than passing the pattern through to discover.)

Test discovery is implemented in ``discover.DiscoveringTestLoader.discover``. As
well as using discover as a command line script you can import
``DiscoveringTestLoader``, which is a subclass of ``unittest.TestLoader``, and
use it in your test framework.

This method finds and returns all test modules from the specified start
directory, recursing into subdirectories to find them. Only test files that
match *pattern* will be loaded. (Using shell style pattern matching.)

All test modules must be importable from the top level of the project. If
the start directory is not the top level directory then the top level
directory must be specified separately.

The ``load_tests`` protocol allows test modules and packages to customize how
they are loaded. This is implemented in
``discover.DiscoveringTestLoader.loadTestsFromModule``. If a test module defines
a ``load_tests`` function then tests are loaded from the module by calling
``load_tests`` with three arguments: `loader`, `standard_tests`, `None`.

If a test package name (directory with `__init__.py`) matches the
pattern then the package will be checked for a ``load_tests``
function. If this exists then it will be called with *loader*, *tests*,
*pattern*.

If ``load_tests`` exists then discovery does  *not* recurse into the package,
``load_tests`` is responsible for loading all tests in the package.

The pattern is deliberately not stored as a loader attribute so that
packages can continue discovery themselves. *top_level_dir* is stored so
``load_tests`` does not need to pass this argument in to
``loader.discover()``.

discover.py is maintained in a google code project (where bugs and feature
requests should be posted): http://code.google.com/p/unittest-ext/

The latest development version of discover.py can be found at:
http://code.google.com/p/unittest-ext/source/browse/trunk/discover.py


CHANGELOG
=========

2010/02/07 0.3.2
----------------

* If ``load_tests`` exists it is passed the standard tests as a ``TestSuite`` 
  rather than a list of tests.

2009/09/13 0.3.1
----------------

* Fixed a problem when a package directory matches the discovery pattern.

2009/08/20 0.3.0
----------------

* Failing to import a file (e.g. due to a syntax error) no longer halts
  discovery but is reported as a failure.
* Discovery will not attempt to import test files whose names are not valid Python
  identifiers, even if they match the pattern.
"""


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      py_modules=MODULES,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS
     )


