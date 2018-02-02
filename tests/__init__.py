import unittest
from .test_clip import TestClip
from .test_full import TestFull


def test_suite():
    return unittest.TestSuite([
        TestClip(),
        TestFull(),
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
