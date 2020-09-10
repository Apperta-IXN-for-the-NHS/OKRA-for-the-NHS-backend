import unittest
from app import app
import json


class RestAPITests(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_get_article_by_id(self):
        response = self.tester.get('/articles/a746226a1bb954106281fcc1cd4bcb7a', content_type='html/text')
        self.assertTrue('200' in response.status)
        self.assertTrue(len(json.loads(response.data)) > 0)

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

    def test_up_vote(self):
        response = self.tester.post('/articles/a746226a1bb954106281fcc1cd4bcb7a/vote',
                                    data=json.dumps({'previous': 0, 'current': 1}),
                                    content_type='application/json')
        self.assertTrue('200' in response.status)

    # def test_down_vote(self):
    #     response = self.tester.post('/articles/a746226a1bb954106281fcc1cd4bcb7a/vote',
    #                                 data=json.dumps({'previous': 0, 'current': -1}),
    #                                 content_type='application/json')
    #     self.assertTrue('200' in response.status)

    def test_cancel_vote(self):
        response = self.tester.post('/articles/a746226a1bb954106281fcc1cd4bcb7a/vote',
                                    data=json.dumps({'previous': 1, 'current': 0}),
                                    content_type='application/json')
        self.assertTrue('200' in response.status)

    def test_vote_illegal_current(self):
        response = self.tester.post('/articles/a746226a1bb954106281fcc1cd4bcb7a/vote',
                                    data=json.dumps({'previous': 1, 'current': 2}),
                                    content_type='application/json')
        self.assertTrue('400' in response.status)

    def test_vote_illegal_previous(self):
        response = self.tester.post('/articles/a746226a1bb954106281fcc1cd4bcb7a/vote',
                                    data=json.dumps({'previous': -2, 'current': 1}),
                                    content_type='application/json')
        self.assertTrue('400' in response.status)

    # def test_add_article(self):
    #     response = self.tester.post('/articles',
    #                                 data=json.dumps({'short_description': 'add_article_test',
    #                                                  'text': 'This is the test for adding articles',
    #                                                  'author': 'wentao'}),
    #                                 content_type='application/json')
    #     print(response, response.status)
    #     self.assertTrue('200' in response.status)

    def test_add_article_missing_author(self):
        response = self.tester.post('/articles',
                                    data=json.dumps({'short_description': 'add_article_test',
                                                     'text': 'This is the test for adding articles'}),
                                    content_type='application/json')
        print(response, response.status)
        self.assertTrue('400' in response.status)

    def test_add_article_missing_title(self):
        response = self.tester.post('/articles',
                                    data=json.dumps({'text': 'This is the test for adding articles',
                                                     'author': 'wentao'}),
                                    content_type='application/json')
        print(response, response.status)
        self.assertTrue('400' in response.status)


if __name__ == '__main__':
    unittest.main()
