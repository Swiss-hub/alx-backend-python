#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        # Arrange: Instantiate the client
        client = GithubOrgClient(org_name)
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Mock get_json to return a specific dict, or just ensure it is called
        mock_get_json.return_value = {"login": org_name}

        # Act: Call the org method
        result = client.org()

        # Assert: get_json is called once with the correct URL
        mock_get_json.assert_called_once_with(expected_url)

        # Assert: the result is as expected (depends on how org() is implemented)
        self.assertEqual(result, {"login": org_name})

if __name__ == '__main__':
    unittest.main()