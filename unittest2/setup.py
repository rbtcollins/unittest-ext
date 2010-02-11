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

DESCRIPTION = 'The new features in unittest for Python 2.7 backported to Python 2.4+.'

URL = 'http://pypi.python.org/pypi/unittest2'

LONG_DESCRIPTION = """
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7. It is tested to run on Python 2.4 - 2.6.""".strip()

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
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS
     )
