import unittest
from app import app

class TestBackendAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_health_endpoint(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "healthy"})

    def test_counter_endpoint(self):
        response = self.client.post('/counter',
                                    json={"increment": 10},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("counter", response.json)

if __name__ == '__main__':
    unittest.main()
