
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
        # In theory this is a step that should be performed, but hg returns
        # a non-zero exit status if it can't figure out what/how to do the merge
        # so for now the step below is left out.  Hopefully a soul wiser than
        # myself can advise on the subject (with advise beyond add '||true')
        # local("hg merge")
        # #################
        os.chdir(os.pardir)
    else:
        local("hg clone %s" % PYTHON_HG_URL)

    if os.path.exists("unittest2"):
        local("rm -rf unittest2")
    shutil.copytree('cpython/Lib/unittest', 'unittest2')
    local("touch unittest2/compatibility.py")
    local("cat unittest2-py3k.patch|patch -p0")


def update_patch():
    """
    Update the patch which is applied to clean checkouts to provided
    backwards compatibility.  The updates are based upon changes to
    the subversion checkout.
    """
    # -u: because they're easier to read (and more svn like which I'm used to)
    # --recursive: go through all files in the tree
    # --new-file: treat absent files as empty, necessary for the compat module
    local("diff -u --recursive --new-file cpython/Lib/unittest unittest2 > unittest2-py3k.patchs || true")



