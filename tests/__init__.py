import unittest
from .test_clip import TestClip
from .test_full import TestFull
from .test_get_tile import TestGetTile
from .test_multi_world import TestMultiWorld


def test_suite():
    return unittest.TestSuite([
        TestClip(),
        TestFull(),
        TestGetTile(),
        TestMultiWorld(),
        ])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
