# setup.py
# Install script for unittest2
# Copyright (C) 2010 Michael Foord
# E-mail: fuzzyman AT voidspace DOT org DOT uk

# This software is licensed under the terms of the BSD license.
# http://www.voidspace.org.uk/python/license.shtml

import sys
from distutils.core import setup
from unittest2 import __version__ as VERSION

NAME = 'configobj'

PACKAGES = ['unittest2', 'unittest2.test']

DESCRIPTION = 'The new features in unittest for Python 2.7 backported to Python 2.4+.'

URL = 'http://pypi.python.org/pypi/unittest2'


LONG_DESCRIPTION = """ """.strip()

CLASSIFIERS = [
    'Development Status :: 6 - Mature',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

AUTHOR = 'Michael Foord'

AUTHOR_EMAIL = 'michael@voidspace.org.uk'

KEYWORDS = "config, ini, dictionary, application, admin, sysadmin, configuration, validation".split(', ')


setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      download_url=DOWNLOAD_URL,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      py_modules=MODULES,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS
     )
