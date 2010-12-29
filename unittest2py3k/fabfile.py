
import os
from fabric.operations import local

# Currently pointing at 3.2 version of unittest
UNITTEST_SVN_URL = "http://svn.python.org/projects/python/branches/py3k/Lib/unittest"
REVISION_FILE = "default-revision.txt"

def create_lib(rev = None):
    """Create the backwards compatible unittest2 library"""
    if os.path.exists("unittest2"):
        local("rm -rf unittest2")
    if not rev:
        with open(REVISION_FILE) as f:
            rev = f.read().strip()
    local("svn co -r %s %s unittest2" % (rev, UNITTEST_SVN_URL))
    local("touch unittest2/compatibility.py")
    local("svn add unittest2/compatibility.py")
    local("cat unittest2-py3k.patch|patch -p0")
    
def update_patch():
    """
    Update the patch which is applied to clean checkouts to provided
    backwards compatibility.  The updates are based upon changes to
    the subversion checkout.
    """
    local("svn diff %s > %s" % ("unittest2", "unittest2-py3k.patch"))


