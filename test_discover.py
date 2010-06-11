import os
import re
import sys

import unittest

if sys.version_info[0] == 2 and sys.version_info[1] < 7: 
    import unittest2
    import unittest2.test
    import_string = 'unittest2'
else:
    unittest2 = unittest
    # probably won't work w/ Python 3.0 / 3.1, tested on Python 3.2 and 2.7
    import unittest.test
    import_string = 'unittest'

from discover import DiscoveringTestLoader

try:
    cmp
except NameError:
    def cmp(x, y):
        """Return -1 if x < y, 0 if x == y and 1 if x > y"""
        return (x > y) - (x < y)

# In Python 2.5 and earlier TestSuites are not comparable
# so we use unittest2.TestSuite for these tests
DiscoveringTestLoader.suiteClass = unittest2.TestSuite


class TestDiscovery(unittest2.TestCase):

    # Heavily mocked tests so I can avoid hitting the filesystem
    def test_get_name_from_path(self):
        loader = DiscoveringTestLoader()

        loader._top_level_dir = '/foo'
        name = loader._get_name_from_path('/foo/bar/baz.py')
        self.assertEqual(name, 'bar.baz')

        if not __debug__:
            # asserts are off
            return

        self.assertRaises(AssertionError,
                          loader._get_name_from_path,
                          '/bar/baz.py')

    def test_find_tests(self):
        loader = DiscoveringTestLoader()

        original_listdir = os.listdir
        def restore_listdir():
            os.listdir = original_listdir
        original_isfile = os.path.isfile
        def restore_isfile():
            os.path.isfile = original_isfile
        original_isdir = os.path.isdir
        def restore_isdir():
            os.path.isdir = original_isdir

        path_lists = [['test1.py', 'test2.py', 'not_a_test.py', 'test_dir',
                       'test.foo', 'test-not-a-module.py', 'another_dir'],
                      ['test3.py', 'test4.py', ]]
        os.listdir = lambda path: path_lists.pop(0)
        self.addCleanup(restore_listdir)

        def isdir(path):
            return path.endswith('dir')
        os.path.isdir = isdir
        self.addCleanup(restore_isdir)

        def isfile(path):
            # another_dir is not a package and so shouldn't be recursed into
            return not path.endswith('dir') and not 'another_dir' in path
        os.path.isfile = isfile
        self.addCleanup(restore_isfile)

        loader._get_module_from_name = lambda path: path + ' module'
        loader.loadTestsFromModule = lambda module: module + ' tests'

        top_level = os.path.abspath('/foo')
        loader._top_level_dir = top_level
        suite = list(loader._find_tests(top_level, 'test*.py'))

        expected = [name + ' module tests' for name in
                    ('test1', 'test2')]
        expected.extend([('test_dir.%s' % name) + ' module tests' for name in
                    ('test3', 'test4')])
        self.assertEqual(suite, expected)

    def test_find_tests_with_package(self):
        loader = DiscoveringTestLoader()

        original_listdir = os.listdir
        def restore_listdir():
            os.listdir = original_listdir
        original_isfile = os.path.isfile
        def restore_isfile():
            os.path.isfile = original_isfile
        original_isdir = os.path.isdir
        def restore_isdir():
            os.path.isdir = original_isdir

        directories = ['a_directory', 'test_directory', 'test_directory2']
        path_lists = [directories, [], [], []]
        os.listdir = lambda path: path_lists.pop(0)
        self.addCleanup(restore_listdir)

        os.path.isdir = lambda path: True
        self.addCleanup(restore_isdir)

        os.path.isfile = lambda path: os.path.basename(path) not in directories
        self.addCleanup(restore_isfile)

        class Module(object):
            paths = []
            load_tests_args = []

            def __init__(self, path):
                self.path = path
                self.paths.append(path)
                if os.path.basename(path) == 'test_directory':
                    def load_tests(loader, tests, pattern):
                        self.load_tests_args.append((loader, tests, pattern))
                        return 'load_tests'
                    self.load_tests = load_tests

            def __eq__(self, other):
                return self.path == other.path

            # Silence py3k warning
            __hash__ = None

        loader._get_module_from_name = lambda name: Module(name)
        def loadTestsFromModule(module, use_load_tests):
            if use_load_tests:
                raise self.failureException('use_load_tests should be False for packages')
            return module.path + ' module tests'
        loader.loadTestsFromModule = loadTestsFromModule

        loader._top_level_dir = '/foo'
        # this time no '.py' on the pattern so that it can match
        # a test package
        suite = list(loader._find_tests('/foo', 'test*'))

        # We should have loaded tests from the test_directory package by calling load_tests
        # and directly from the test_directory2 package
        self.assertEqual(suite,
                         ['load_tests', 'test_directory2' + ' module tests'])
        self.assertEqual(Module.paths, ['test_directory', 'test_directory2'])

        # load_tests should have been called once with loader, tests and pattern
        self.assertEqual(Module.load_tests_args,
                         [(loader, 'test_directory' + ' module tests', 'test*')])

    def test_discover(self):
        loader = DiscoveringTestLoader()

        original_isfile = os.path.isfile
        original_isdir = os.path.isdir
        def restore_isfile():
            os.path.isfile = original_isfile

        os.path.isfile = lambda path: False
        self.addCleanup(restore_isfile)

        orig_sys_path = sys.path[:]
        def restore_path():
            sys.path[:] = orig_sys_path
        self.addCleanup(restore_path)

        full_path = os.path.abspath(os.path.normpath('/foo'))
        self.assertRaises(ImportError,
                          loader.discover,
                          '/foo/bar', top_level_dir='/foo')

        self.assertEqual(loader._top_level_dir, full_path)
        self.assertIn(full_path, sys.path)

        os.path.isfile = lambda path: True
        os.path.isdir = lambda path: True

        def restore_isdir():
            os.path.isdir = original_isdir
        self.addCleanup(restore_isdir)

        _find_tests_args = []
        def _find_tests(start_dir, pattern):
            _find_tests_args.append((start_dir, pattern))
            return ['tests']
        loader._find_tests = _find_tests
        loader.suiteClass = str

        suite = loader.discover('/foo/bar/baz', 'pattern', '/foo/bar')

        top_level_dir = os.path.abspath(os.path.normpath('/foo/bar'))
        start_dir = os.path.abspath(os.path.normpath('/foo/bar/baz'))
        self.assertEqual(suite, "['tests']")
        self.assertEqual(loader._top_level_dir, top_level_dir)
        self.assertEqual(_find_tests_args, [(start_dir, 'pattern')])
        self.assertIn(top_level_dir, sys.path)

    def test_discover_with_modules_that_fail_to_import(self):
        loader = DiscoveringTestLoader()

        listdir = os.listdir
        os.listdir = lambda _: ['test_this_does_not_exist.py']
        isfile = os.path.isfile
        os.path.isfile = lambda _: True
        orig_sys_path = sys.path[:]
        def restore():
            os.path.isfile = isfile
            os.listdir = listdir
            sys.path[:] = orig_sys_path
        self.addCleanup(restore)

        suite = loader.discover('.')
        self.assertIn(os.getcwd(), sys.path)
        self.assertEqual(suite.countTestCases(), 1)
        test = list(list(suite)[0])[0] # extract test from suite

        self.assertRaises(ImportError,
            lambda: test.test_this_does_not_exist())

    def test_detect_module_clash(self):
        class Module(object):
            __file__ = 'bar/foo.py'
        sys.modules['foo'] = Module
        full_path = os.path.abspath('foo')
        original_listdir = os.listdir
        original_isfile = os.path.isfile
        original_isdir = os.path.isdir
        
        def cleanup():
            os.listdir = original_listdir
            os.path.isfile = original_isfile
            os.path.isdir = original_isdir
            del sys.modules['foo']
            if full_path in sys.path:
                sys.path.remove(full_path)
        self.addCleanup(cleanup)
        
        def listdir(_):
            return ['foo.py']
        def isfile(_):
            return True
        def isdir(_):
            return True
        os.listdir = listdir
        os.path.isfile = isfile
        os.path.isdir = isdir
        
        loader = DiscoveringTestLoader()
        
        mod_dir = os.path.abspath('bar')
        expected_dir = os.path.abspath('foo')
        msg = re.escape(r"'foo' module incorrectly imported from %r. Expected %r. "
                "Is this module globally installed?" % (mod_dir, expected_dir))
        self.assertRaisesRegexp(
            ImportError, '^%s$' % msg, loader.discover,
            start_dir='foo', pattern='foo.py'
        )
        self.assertEqual(sys.path[0], full_path)

        
    def test_discovery_from_dotted_path(self):
        loader = DiscoveringTestLoader()
        
        tests = [self]
        expectedPath = os.path.abspath(os.path.dirname(unittest2.test.__file__))

        self.wasRun = False
        def _find_tests(start_dir, pattern):
            self.wasRun = True
            self.assertEqual(start_dir, expectedPath)
            return tests
        loader._find_tests = _find_tests
        suite = loader.discover('%s.test' % import_string)
        self.assertTrue(self.wasRun)
        self.assertEqual(suite._tests, tests)


if __name__ == '__main__':
    unittest2.main()
