#!/usr/bin/env python3
@parameterized.expand([
    ("nested_map_simple", {"a": 1}, ("a",), 1),
    ("nested_map_nested", {"a": {"b": 2}}, ("a",), {"b": 2}),
    ("nested_map_deep", {"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, name, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)