#!/usr/bin/env python3
'''unit test for client methodes'''
from client import GithubOrgClient
from utils import get_json
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class  # type: ignore
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


@parameterized_class([
    {'org_payload': TEST_PAYLOAD[0][0],
     'repos_payload': TEST_PAYLOAD[0][1],
     'expected_repos': TEST_PAYLOAD[0][2],
     'apache2_repos': TEST_PAYLOAD[0][3]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    '''TestGithubOrgClient class'''
    @classmethod
    def setUpClass(cls) -> None:
        """init the class"""

        def return_pld(url) -> Mock:
            """return the mock"""
            data = None
            if url == 'https://api.github.com/orgs/google':
                data = cls.org_payload
            elif url == 'https://api.github.com/orgs/google/repos':
                data = cls.repos_payload
            else:
                return None
            return Mock(json=Mock(return_value=data))

        cls.get_patcher = patch('requests.get', side_effect=return_pld)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the public_repos method."""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Tests the public_repos with license method."""
        client = GithubOrgClient('google')
        self.assertEqual(client.public_repos('apache-2.0'), self.apache2_repos)

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class"""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
