from locust import TaskSet, task, HttpUser


class Tasks(TaskSet):
    @task
    def get_article_by_id(self):
        article_id = '65bba7181b42901064244375cc4bcb61'
        self.client.get(f'/articles/{article_id}', name='/articles/id')

    @task
    def get_articles(self):
        self.client.get('/articles')

    @task
    def get_articles_with_limit_and_start(self):
        start = 1
        limit = 1
        self.client.get(f'/articles?start={start}&limit={limit}', name='/articles')

    @task
    def get_articles_with_query(self):
        query_term = "test"
        start = 1
        limit = 1
        self.client.get(f'/articles?query={query_term}&start={start}&limit={limit}', name='/articles?query')

    @task
    def up_vote(self):
        article_id = '65bba7181b42901064244375cc4bcb61'
        data = {"previous": 0, "current": 1}
        self.client.post(f'/articles/{article_id}/vote', json=data, name='/articles/id/vote')

    @task
    def down_vote(self):
        article_id = '65bba7181b42901064244375cc4bcb61'
        data = {"previous": 0, "current": -1}
        self.client.post(f'/articles/{article_id}/vote', json=data, name='/articles/id/vote')

    @task
    def get_cases_with_limit_and_start(self):
        start = 1
        limit = 1
        self.client.get(f'/cases?start={start}&limit={limit}', name='/cases')

    @task
    def get_cases_with_query(self):
        query_term = "case"
        start = 1
        limit = 1
        self.client.get(f'/cases?query={query_term}&start={start}&limit={limit}', name='/cases?query')


class User(HttpUser):
    # need to be changed
    host = 'WEBSITE_URL'

    tasks = [Tasks]
    min_wait = 1000
    max_wait = 5000
