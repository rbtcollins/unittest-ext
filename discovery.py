import os
import sys
from unittest import TextTestRunner, TestLoader
from fnmatch import fnmatch

        
class DiscoveringLoader(TestLoader):
    
    _top_level_dir = None
    
    def loadTestsFromModule(self, module, use_load_tests=True):
        """This method adds the 'load_tests' protocol to test modules
        to allow them to customize test loading."""
        tests = TestLoader.loadTestsFromModule(self, module)
        load_tests = getattr(module, 'load_tests', None)
        if use_load_tests and load_tests is not None:
            # load_tests is a hook allowing test modules to customize
            # how tests are loaded.
            # Arguments passsed into the load_tests function are:
            # loader, tests and discovery pattern
            # For modules None is always passed in for the pattern
            # parameter (the third parameter).
            tests = load_tests(self, tests, None)
        return tests
    
    def discover(self, start_dir, include_filter='test*', top_level_dir=None):
        """Find and return all test modules from the specified start directory, recursing
        into subdirectories to find them. Only test files that match the filter will
        be loaded.
        
        All test modules must be importable from the top level of the project. If
        the start directory is not the top level directory then the top level
        directory must be specified separately.
        
        If a test package name (directory with '__init__.py') matches the include
        filter then the package will be checked for a 'load_tests' function. If
        this exists then it will be called with loader, None, include_filter.
        
        If load_tests exists then discovery does  *not* recurse into the package,
        load_tests is responsible for loading all tests in the package.
        
        The include_filter is deliberately not stored as a loader attribute so that
        packages can continue discovery themselves. top_level_dir is stored so 
        load_tests does not need to pass this argument in to loader.discover().
        """
        if top_level_dir is None and self._top_level_dir is not None:
            # make top_level_dir optional if called from load_tests in a package
            top_level_dir = self._top_level_dir
        elif top_level_dir is None:
            top_level_dir = start_dir
            
        top_level_dir = os.path.abspath(os.path.normpath(top_level_dir))
        start_dir = os.path.abspath(os.path.normpath(start_dir))
    
        if not top_level_dir in sys.path:
            # all test modules must be importable from the top level directory
            sys.path.append(top_level_dir)
        self._top_level_dir = top_level_dir
        
        if start_dir != top_level_dir and not os.path.isfile(os.path.join(start_dir, '__init__.py')):
            # what about __init__.pyc or pyo (etc)
            raise ImportError('Start directory is not importable: %r' % start_dir)
        
        tests = list(self._find_tests(start_dir, include_filter))
        return self.suiteClass(tests)
    

    def _find_tests(self, start_dir, include_filter):
        paths = os.listdir(start_dir)
        
        for path in paths:
            full_path = os.path.join(start_dir, path)
            # what about __init__.pyc or pyo (etc)
            # we would need to avoid loading the same tests multiple times
            # from '.py', '.pyc' *and* '.pyo'
            if os.path.isfile(full_path) and path.lower().endswith('.py'):
                if fnmatch(path, include_filter):
                    # if the test file matches, load it
                    module = self._get_module_from_path(full_path)
                    yield self.loadTestsFromModule(module)
                    
            elif os.path.isdir(full_path):
                # what about __init__.pyc or pyo (etc)
                if not os.path.isfile(os.path.join(full_path, '__init__.py')):
                    # skip subdirectories that aren't packages
                    continue
                
                load_tests = None
                tests = None
                if fnmatch(path, include_filter):
                    # only check load_tests if the package directory itself matches the filter
                    package = self._get_module_from_path(full_path)
                    load_tests = getattr(package, 'load_tests', None)
                    tests = self.loadTestsFromModule(package, use_load_tests=False)
                
                if load_tests is None:
                    if tests is not None and tests.countTestCases() > 0:
                        # tests loaded from package file
                        yield tests
                    # recurse into the package
                    for test in self._find_tests(full_path, include_filter):
                        yield test
                else:
                    yield load_tests(self, tests, include_filter)
        
    def _get_module_from_path(self, path):
        """Load a module from a path relative to the top-level directory
        of a project. Used by discovery."""
        path = os.path.splitext(os.path.normpath(path))[0]
        
        relpath = os.path.relpath(path, self._top_level_dir)
        assert not os.path.isabs(relpath), "Path must be within the project"
        assert not relpath.startswith('..'), "Path must be within the project"
        
        name = relpath.replace(os.path.sep, '.')
        __import__(name)
        return sys.modules[name]
        

def discover(start_dir='.', include_filter='test*', top_level_dir=None, **kwargs):
    """Find and run all test modules from the specified start directory, recursing
    into subdirectories to find them. Only test files that match the filter will
    be loaded.
    
    All test modules must be importable from the top level of the project. If
    the start directory is not the top level directory then the top level
    directory must be specified separately.
    
    Tests are run with a TextTestRunner. Extra keyword arguments passed to
    discover are passed through to the TextTestRunner.
    
    The result object returned by TextTestRunner.run() is returned.
    """
    loader = DiscoveringLoader()
    suite = loader.discover(start_dir, include_filter, top_level_dir)
    
    return TextTestRunner(**kwargs).run(suite)

    
if __name__ == '__main__':
    # my intention is to build test discovery into unittest command line usage with the form
    # python -m unittest discover start_dir include_filter top_level_directory
    result = discover(*sys.argv[1:])
    sys.exit(not result.wasSuccessful())

# If the start directory is a package, we don't load tests from it's __init__.py
# instead we start discovery *inside* the package.
    
# load_tests for module is called with (loader, tests, None)
# load_tests for package (only used from discovery) is called with (loader, tests, include_filter)

# uses os.path.relpath so requires Python 2.6+

# doesn't handle __path__ for test packages that extend themselves in odd ways

# all tests must be in valid packages and importable from the top level of the project
# recognises packages through an explicit '__init__.py' file - no allowance for .pyo, .pyc, .so, .pyd, .zip etc

# should use code from load_from_dir in:
# http://bazaar.launchpad.net/~bzr/bzr/trunk/annotate/head%3A/bzrlib/plugin.py
