import random
from locust import TaskSet, task, HttpUser


class Tasks(TaskSet):
    @task(4)
    def get_article_by_id(self):
        article_id = '223131ea1bb1d0106281fcc1cd4bcbc9'
        self.client.get(f'/articles/{article_id}', name='/articles/id')

    @task
    def get_articles(self):
        self.client.get('/articles')

    @task
    def get_articles_with_limit(self):
        self.client.get(f'/articles?limit={random.randint(0,11)}', name='/articles')

    @task
    def get_articles_with_start(self):
        self.client.get(f'/articles?start={random.randint(0,11)}', name='/articles')

    @task
    def get_articles_with_limit_and_start(self):
        self.client.get(f'/articles?start={random.randint(0,11)}&limit={random.randint(0,11)}', name='/articles')

class User(HttpUser):
    host = 'http://162.62.53.126:4123'
    tasks = [Tasks]
    min_wait = 1000
    max_wait = 5000