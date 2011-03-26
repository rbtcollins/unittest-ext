
import os
import shutil
from fabric.operations import local

PYTHON_HG_URL = 'http://hg.python.org/cpython/'
REVISION_FILE = "default-revision.txt"

def create_lib(rev = None):
    """Create the backwards compatible unittest2 library"""
    if not rev:
        with open(REVISION_FILE) as f:
            rev = f.read().strip()
    if os.path.exists("cpython"):
        os.chdir("cpython")
        local("hg pull")
        local("hg update")
        os.chdir(os.pardir)
    else:
        local("hg clone %s" % PYTHON_HG_URL)

    if os.path.exists("unittest2"):
        local("rm -rf unittest2")
    shutil.copytree('cpython/Lib/unittest', 'unittest2')
    local("touch unittest2/compatibility.py")
    #local("cat unittest2-py3k.patch|patch -p0")


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



