import unittest
import test
"""
This was added so that pytest could correctly find the test cases.
If you run the script it should run the tests through unittests'
text test runner.
ex. python test.py
"""

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    test_runner = unittest.TextTestRunner()
    test_runner.run(test_suite)
