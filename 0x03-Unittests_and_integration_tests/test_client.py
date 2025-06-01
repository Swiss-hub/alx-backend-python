#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):

  @parameterized.expand([
    ("google",),
    ("abc",),
  ])
  @patch('client.get_json')
  def test_org(self, org_name, mock_get_json):
    client = GithubOrgClient(org_name)
    expected_url = f"https://api.github.com/orgs/{org_name}"
    mock_get_json.return_value = {"login": org_name}
    result = client.org()
    mock_get_json.assert_called_once_with(expected_url)
    self.assertEqual(result, {"login": org_name})

  @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
  def test_public_repos_url(self, mock_org):
    mock_org.return_value = {"repos_url": "http://some_url"}
    client = GithubOrgClient("test_org")
    self.assertEqual(client._public_repos_url, "http://some_url")

  @patch('client.get_json')
  @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
  def test_repos_payload(self, mock_public_repos_url, mock_get_json):
    mock_public_repos_url.return_value = "http://some_url"
    mock_get_json.return_value = [{"id": 1}]
    client = GithubOrgClient("test_org")
    self.assertEqual(client.repos_payload, [{"id": 1}])
    mock_get_json.assert_called_once_with("http://some_url")

  @patch('client.GithubOrgClient.repos_payload', new_callable=PropertyMock)
  def test_public_repos(self, mock_repos_payload):
    mock_repos_payload.return_value = [
      {"name": "repo1", "license": {"key": "mit"}},
      {"name": "repo2", "license": {"key": "apache-2.0"}},
      {"name": "repo3"}
    ]
    client = GithubOrgClient("test_org")
    # No license filter
    self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
    # With license filter
    self.assertEqual(client.public_repos(license="mit"), ["repo1"])
    self.assertEqual(client.public_repos(license="apache-2.0"), ["repo2"])
    self.assertEqual(client.public_repos(license="gpl"), [])

  @patch('client.GithubOrgClient.repos_payload', new_callable=PropertyMock)
  def test_public_repos_with_license(self, mock_repos_payload):
        """Test public_repos returns only repos with the specified license."""
        mock_repos_payload.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3"}
        ]
        client = GithubOrgClient("test_org")
        expected = ["repo2"]
        self.assertEqual(client.public_repos(license="apache-2.0"), expected)

  def test_has_license(self):
    repo = {"license": {"key": "mit"}}
    self.assertTrue(GithubOrgClient.has_license(repo, "mit"))
    self.assertFalse(GithubOrgClient.has_license(repo, "apache-2.0"))
    repo_no_license = {}
    self.assertFalse(GithubOrgClient.has_license(repo_no_license, "mit"))

if __name__ == '__main__':
  unittest.main()