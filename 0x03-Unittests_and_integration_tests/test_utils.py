#!/usr/bin/env python3
'''unit test for utils methodes'''
import unittest
access_nested_map = __import__('utils').access_nested_map


class TestAccessNestedMap(unittest.TestCase):

    def test_access_nested_map(self):
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a", "b")), 2)


if __name__ == '__main__':
    unittest.main()
