
import os
import shutil
import ConfigParser
from fabric.operations import local
from contextlib import contextmanager

PYTHON_HG_URL = 'http://hg.python.org/cpython/'
CPYTHON_INI = "hg-cpython.ini"

@contextmanager
def enter_dir(dirname):
    orig_dir = os.getcwd()
    os.chdir(dirname)
    yield
    os.chdir(orig_dir)


def create_lib(rev = None):
    """Create the backwards compatible unittest2 library"""

    # Get or update the cpython hg repo
    if os.path.exists("cpython"):
        with enter_dir("cpython"):
            # local("hg pull")
            pass
            # local("hg update") Delete?
    else:
        local("hg clone %s" % PYTHON_HG_URL)

    # Switch to the desired branch/revision
    cfg = ConfigParser.ConfigParser()
    cfg.read(CPYTHON_INI)
    branch = cfg.get('default', 'branch')
    rev = cfg.get('default', 'revision')

    with enter_dir("cpython"):
        local("hg update -C %s" % branch)
        local("hg revert --no-backup -r %s Lib/unittest" % rev)
            
    # Remove the old copy of lib if exists
    if os.path.exists("unittest2"):
        local("rm -rf unittest2")
    shutil.copytree('cpython/Lib/unittest', 'unittest2')
    local("touch unittest2/compatibility.py")
    local("cat unittest2-py3k.patch|patch -p0 --no-backup-if-mismatch")


def update_patch():
    """
    Update the patch which is applied to clean checkouts to provided
    backwards compatibility.  The updates are based upon changes to
    the subversion checkout.
    """
    # -u: because they're easier to read (and more svn like which I'm used to)
    # -x '*.pyc': Don't do diff's on pyc files
    # --recursive: go through all files in the tree
    # --new-file: treat absent files as empty, necessary for the compat module
    # ||true: diff returns 1 if any differences are found, prevents fab complaining
    src = "unittest2"
    patch_file = 'unittest2-py3k.patch'
    local("diff -u -x '*.pyc' --recursive --new-file cpython/Lib/unittest %s > %s || true" % (src, patch_file))



