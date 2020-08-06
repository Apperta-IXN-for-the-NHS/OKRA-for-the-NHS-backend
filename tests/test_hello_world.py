import unittest
from emisbackend import app


class MyTestCase(unittest.TestCase):
    def test_hello_world(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.data, b'Hello World!')


if __name__ == '__main__':
    unittest.main()
