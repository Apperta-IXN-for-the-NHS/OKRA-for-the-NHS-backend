import json
import unittest
from app import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_add_case(self):
        response = self.tester.post('/cases',
                                    data=json.dumps({'title': '1000', 'body': '1000', 'priority': 2}),
                                    content_type='application/json')
        self.assertTrue('200' in response.status)

    def test_add_case_with_less_data(self):
        response = self.tester.post('/cases',
                                    data=json.dumps({'title': '1000', 'priority': 2}),
                                    content_type='application/json')
        self.assertTrue('400' in response.status)

if __name__ == '__main__':
    unittest.main()
