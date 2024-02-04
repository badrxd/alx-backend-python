#!/usr/bin/env python3
'''unit test for utils methodes'''
from utils import get_json, memoize
from parameterized import parameterized
import unittest
from unittest.mock import patch, Mock
access_nested_map = __import__('utils').access_nested_map


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, result):
        self.assertEqual(access_nested_map(nested_map, path), result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):

    @parameterized.expand([
        ('http://example.com', True),
        ('http://holberton.io', False),
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, get_json_pld):
        sent_req = Mock()
        sent_req.json.return_value = {"payload": test_payload}
        get_json_pld.return_value = sent_req
        self.assertEqual(get_json(test_url)['payload'], test_payload)
        get_json_pld.assert_called_with(test_url)


class TestMemoize(unittest.TestCase):
    """Tests the memoize methode."""

    def test_memoize(self) -> None:
        """Tests memoize output."""
        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=lambda: 42
                          ) as mock_a_method:
            call = TestClass()
            self.assertEqual(call.a_property(), 42)
            mock_a_method.assert_called_once()
            self.assertEqual(call.a_property(), 42)
            mock_a_method.assert_called_once()
