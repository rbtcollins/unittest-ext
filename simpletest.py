import unittest2


class Test(unittest2.TestCase):
    def testFail(self):
        self.fail("oops")

def test_something():
    assert 3 == 2



def make_load_tests(module_name):
    import sys
    import unittest2
        
    module = sys.modules[module_name]
    def load_tests(loader, tests, pattern):
        these_tests = []
        for entry, obj in module.__dict__.items():
            if entry.lower().startswith('test') and callable(obj) and not isinstance(obj, type):
                these_tests.append(unittest2.FunctionTestCase(obj))
        tests.addTests(unittest2.TestSuite(these_tests))
        return tests
    return load_tests
    
    
load_tests = make_load_tests(__name__)

if __name__ == '__main__':
    unittest2.main()