# OKRA Backend

This is the backend of Open Knowledge Rank (OKRA).

## REST APIs

### Get an article by ID

GET /articles/{article_id}

replace {article_id} with string

Returned JSON format:

```json
{
    "id": "string",
    "title": "string",
    "author": "string",
    "created": "string",
    "body": "string",
    "view_count": 0,
    "net_votes": 0,
    "related": [
        {
            "id": "string",
            "title": "string",
            "author": "string",
            "created": "string",
            "view_count": 0,
            "net_votes": 0
        }
    ]
}
```

### Get articles sorted by trending and similarity

GET /articles?limit={limit_num}&start={start_index}&query={query_term}

replace {limit_num} and {start_index} with integer, {query_term} with string

Optional parameters:

- limit: the number of shown articles
- start: the start index
- query: search term

Returned JSON format:

```json
[
    {
        "id": "string",
        "title": "string",
        "author": "string",
        "created": "string: 2020-08-01",
        "view_count": 0,
        "net_votes": 0
    }
]
```

### Vote articles

POST /articles/{article_id}/vote

replace {article_id} with string

previous and current could be -1, 0 and 1

Accept JSON format:

```json
{
    "previous": 0,
    "current": 1
}
```

### Add an article

POST /articles

Accept JSON format:

```json
{
    "short_description": "string",
    "author": "string",
    "text": "string"
}
```

There could be other optional keys: number, kb_category, article_type, kb_knowledge_base, published, sys_tags, sys_view_count


### Get a case by id

GET /cases/{case_id}

replace {case_id} with string

Priority is between 1 to 4, 1 represents the highest priority.

Returned JSON format:

```json
{
    "id": "string",
    "title": "string",
    "body": "string",
    "priority": 1,
    "date": "string"
}
```

### Get cases sorted by date and priority

GET /cases?limit={limit_num}&start={start_index}&query={query_term}

replace {limit_num} and {start_index} with integer, {query_term} with string

Optional parameters:

- limit: the number of shown cases
- start: the start index
- query: search term

Priority is between 1 to 4, 1 represents the highest priority.

Returned JSON format:

```json
[
    {
        "id": "string",
        "title": "string",
        "body": "string",
        "priority": 1,
        "date": "string"
    }
]
```

### Add a case

POST /cases

Priority is between 1 to 4, 1 represents the highest priority.

Accept JSON format:

```json
{
    "title": "string",
    "body": "string",
    "priority": 1
}
```

## Tests

### Unit Testing

Unit Testing is done by unittest. The test files will be executed automatically in the continuous integration.

```cmd
python tests/unittest/test_knowledge_endpoint.py
python tests/unittest/test_case_endpoint.py
```

### Performance Testing

Performance Testing is done by Locust.

1. Go to tests/locust dir

   ```cmd
   cd tests/locust
   ```

2. Run Locust

   - Command Line Interface

     - -u: number of users

     - -r: hatch rate, number of users generated per second

     - -t: run time, terminate after specified time

     - --headless: headless mode

       ```cmd
       locust -u 500 -r 100 -t 5m --headless
       ```

   - Graphical User Interface

     - command

       ```cmd
       locust
       ```

     - visit http://127.0.0.1:8089/ and input parameter values

## Reuse

If you want to reuse the backend application, please follow the instruction below.

1. make sure Docker is installed locally and opened

2. clone the repo to local

    ```cmd
    git clone https://github.com/Apperta-IXN-for-the-NHS/OKRA-for-the-NHS-backend.git
    ```

3. go to `app/__init__.py` and find the following statement, change to your database connection url

    ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = "DB_CONNECTION_URL"
    ```

4. build Docker file

    ```cmd
    docker build -t 'okra-backend' .
    ```

5. run Docker (specify the port you want to use, e.g. 4123)

    ```cmd
    docker run -d -p 4123:80 okra-backend
    ```

### Testing

1. go to `tests/locust/locustfile.py` and find the following statement, change to your website url 

    ```python
   host = 'WEBSITE_URL'
    ```

2. To enable unit testing and performance testing, test cases in `tests/locust/locustfile.py`, `tests/unittest/test_case_endpoint.py` and `tests/unittest/test_knowledge_endpoint.py` need to be changed according to the valid data in your database.
