import json
import unittest
from app import app


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_case_by_id(self):
        response = self.tester.get('/cases/076f1eee8d564ab19b13edcb8cfccc42')
        self.assertTrue('200' in response.status)
        self.assertEqual(json.loads(response.data)['title'], 'case a')

    def test_get_case_by_wrong_id(self):
        response = self.tester.get('/cases/111')
        self.assertTrue('404' in response.status)

    def test_get_cases_with_no_param(self):
        response = self.tester.get('/cases')
        self.assertTrue('200' in response.status)
        self.assertTrue(len(json.loads(response.data)) > 0)

    def test_get_cases_with_limit(self):
        response = self.tester.get('/cases?limit=2')
        self.assertTrue('200' in response.status)
        self.assertTrue(len(json.loads(response.data)) > 0)

    def test_get_cases_with_start(self):
        response = self.tester.get('/cases?start=1')
        self.assertTrue('200' in response.status)
        self.assertTrue(len(json.loads(response.data)) > 0)

    def test_get_cases_with_query(self):
        response = self.tester.get('/cases?query=test')
        self.assertTrue('200' in response.status)
        self.assertTrue(len(json.loads(response.data)) > 0)

    def test_get_cases_with_multiple_params(self):
        response = self.tester.get('/cases?query=test&limit=2&start=1')
        self.assertTrue('200' in response.status)
        self.assertTrue(len(json.loads(response.data)) > 0)

    # def test_add_case(self):
    #     response = self.tester.post('/cases',
    #                                 data=json.dumps({'title': '1000', 'body': '1000', 'priority': 2}),
    #                                 content_type='application/json')
    #     self.assertTrue('200' in response.status)

    def test_add_case_missing_body(self):
        response = self.tester.post('/cases',
                                    data=json.dumps({'title': '1000', 'priority': 2}),
                                    content_type='application/json')
        self.assertTrue('400' in response.status)

    def test_add_case_missing_title(self):
        response = self.tester.post('/cases',
                                    data=json.dumps({'body': '1000', 'priority': 2}),
                                    content_type='application/json')
        self.assertTrue('400' in response.status)


if __name__ == '__main__':
    unittest.main()
