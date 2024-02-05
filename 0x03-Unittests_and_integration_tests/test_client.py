#!/usr/bin/env python3
'''unit test for client methodes'''
from client import GithubOrgClient
from utils import get_json
from parameterized import parameterized  # type: ignore
import unittest
from unittest.mock import patch, Mock, PropertyMock, MagicMock


class TestGithubOrgClient(unittest.TestCase):
    '''TestGithubOrgClient class'''

    @parameterized.expand(["google", "abc"])
    @patch('client.get_json',)
    def test_org(self, org: str, get_json: Mock) -> None:
        '''method test that GithubOrgClient.org
        returns the correct value.'''
        data = Mock()
        data.return_value = {'org': org}
        get_json.return_value = data
        client = GithubOrgClient(org)
        test_1 = client.org()
        test_2 = client.org()
        self.assertEqual(test_1, test_2)
        get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self):
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/users/google/repos"}
            url = GithubOrgClient('google')._public_repos_url
            self.assertEqual(url, "https://api.github.com/users/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, payload: MagicMock) -> None:
        '''Tests the public_repos method'''
        data = MagicMock(return_value=[{'name': "badr"}, {"name": "badrxd"}])
        payload.return_value = data()
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as url:
            url.return_value = "https://api.github.com/users/google/repos"
            call = GithubOrgClient('google').public_repos()
            self.assertEqual(call, ['badr', 'badrxd'])
            self.assertIsInstance(call, list)
            url.assert_called_once()
            payload.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, 'my_license', True),
        ({"license": {"key": "other_license"}}, 'my_license', False)
    ])
    def test_has_license(self, repo, license_key, bl):
        client = GithubOrgClient('google')
        self.assertEqual(client.has_license(repo, license_key), bl)


if __name__ == "__main__":
    unittest.main()
