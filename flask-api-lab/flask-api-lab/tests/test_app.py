import unittest
from unittest.mock import MagicMock, patch

import requests
from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def upstream(self, data, status=200):
        response = MagicMock()
        response.status_code = status
        response.json.return_value = data
        if status >= 400:
            response.raise_for_status.side_effect = requests.HTTPError()
        response.__enter__.return_value = response
        return response

    def test_home_and_health(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/api/health').json, {'ok': True})

    @patch('app.requests.get')
    def test_success(self, get):
        url = 'https://images.dog.ceo/breeds/hound/test.jpg'
        get.return_value = self.upstream({'status': 'success', 'message': url})
        result = self.client.get('/api/dog')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['image_url'], url)
        self.assertIn('timeout', get.call_args.kwargs)

    @patch('app.requests.get', side_effect=requests.Timeout())
    def test_timeout(self, get):
        self.assertEqual(self.client.get('/api/dog').status_code, 504)

    @patch('app.requests.get')
    def test_http_failure_and_rate_limit(self, get):
        for upstream_status, expected in [(500, 502), (404, 502), (429, 503)]:
            with self.subTest(upstream_status=upstream_status):
                get.return_value = self.upstream({}, upstream_status)
                self.assertEqual(self.client.get('/api/dog').status_code, expected)

    @patch('app.requests.get')
    def test_invalid_json(self, get):
        get.return_value = self.upstream({})
        get.return_value.json.side_effect = ValueError('invalid')
        self.assertEqual(self.client.get('/api/dog').status_code, 502)

    @patch('app.requests.get')
    def test_invalid_fields_and_urls(self, get):
        cases = [[], {}, {'status': 'error'}, {'status': 'success'},
                 {'status': 'success', 'message': ['not-a-string']}]
        for url in ['http://images.dog.ceo/a.jpg', 'https://evil.example/a.jpg',
                    'https://images.dog.ceo.evil.example/a.jpg',
                    'https://user@images.dog.ceo/a.jpg',
                    'https://images.dog.ceo:8080/a.jpg',
                    'https://images.dog.ceo:bad/a.jpg']:
            cases.append({'status': 'success', 'message': url})
        for data in cases:
            with self.subTest(data=data):
                get.return_value = self.upstream(data)
                response = self.client.get('/api/dog')
                self.assertEqual(response.status_code, 502)
                self.assertFalse(response.json['ok'])


if __name__ == '__main__':
    unittest.main()
