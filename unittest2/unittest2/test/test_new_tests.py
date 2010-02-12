import os
import sys

if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

import unittest
import unittest2


class TestUnittest(unittest2.TestCase):
    
    def assertIsSubclass(self, actual, klass):
        self.assertTrue(issubclass(actual, klass), "Not a subclass.")
    
    def testInheritance(self):
        self.assertIsSubclass(unittest2.TestCase, unittest.TestCase)
        self.assertIsSubclass(unittest2.TestResult, unittest.TestResult)
        self.assertIsSubclass(unittest2.TestSuite, unittest.TestSuite)
        
        
        
if __name__ == '__main__':
    unittest2.main()