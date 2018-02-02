import unittest
from .test_full import TestFull


def test_suite():
    return unittest.TestSuite([
        TestFull(),
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
