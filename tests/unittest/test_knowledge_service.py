import unittest
from app import app
import json


class RestAPITests(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_article_by_id(self):
        response = json.loads(
            self.tester.get('/articles/223131ea1bb1d0106281fcc1cd4bcbc9', content_type='html/text').data)
        self.assertEqual(response['id'], '223131ea1bb1d0106281fcc1cd4bcbc9')
        self.assertEqual(response['author'], 'Michael Sheary')
        self.assertEqual(response['created'], "2020-07-07")
        self.assertEqual(response['title'], 'EMIS Web third party network access advisory')
        self.assertIsNotNone(response['body'])
        self.assertTrue(len(response['related']) >= 0)

        for article in response['related']:
            self.assertIsNotNone(article['id'])
            self.assertIsNotNone(article['created'])
            self.assertIsNotNone(article['author'])
            self.assertIsNotNone(article['title'])
            self.assertIsNotNone(article['view_count'])

    def test_get_not_existing_articles(self):
        response = json.loads(self.tester.get('/articles/1', content_type='html/text').data)
        self.assertTrue(len(response) == 0)

    def test_get_recent_articles_no_parameter(self):
        response = json.loads(self.tester.get('/articles', content_type='html/text').data)
        self.assertEqual(len(response), 5)

        for article in response:
            self.assertIsNotNone(article['id'])
            self.assertIsNotNone(article['created'])
            self.assertIsNotNone(article['author'])
            self.assertIsNotNone(article['title'])

    def test_get_recent_articles_with_limit(self):
        response = json.loads(self.tester.get('/articles?limit=3', content_type='html/text').data)
        self.assertEqual(len(response), 3)

    def test_get_recent_articles_with_start_and_limit(self):
        response = json.loads(self.tester.get('/articles?start=1&limit=3', content_type='html/text').data)
        self.assertEqual(len(response), 3)


if __name__ == '__main__':
    unittest.main()
