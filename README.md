# Emis Backend

This is the backend of OKRA in EMIS project.

## REST APIs

VPS IP Address: 162.62.53.126

Port: 4123

### Get an article by ID

GET 162.62.53.126:4123/articles/{article_id}

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

GET 162.62.53.126:4123/articles?limit={limit_num}&start={start_index}&query={query_term}

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

POST 162.62.53.126:4123/articles/{article_id}/vote

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

POST 162.62.53.126:4123/articles

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

GET 162.62.53.126:4123/cases/{case_id}

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

GET 162.62.53.126:4123/cases?limit={limit_num}&start={start_index}&query={query_term}

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

POST 162.62.53.126:4123/cases

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

## Docker

**Attention**: On our VPS, the Gunicorn server of the back-end application uses the port 41234, and the Nginx server mapping port 41234 to port 4123. If you visit port 41234, requests will be handled by Gunicorn directly. If you visit port 4123, requests will be handled by Gunicorn + Nginx.

If you want to use the back-end application, first make sure Docker is installed locally

### Clone & Build

1. clone the repo to local

   ```cmd
   git clone https://github.com/Went-Yang/emis-backend.git
   ```

2. build docker file

   ```cmd
   docker build -t 'emis-backend' .
   ```

3. run docker

   ```cmd
   docker run -d -p 4123:80 emis-backend
   ```


### Pull from Docker Hub

1. pull the docker files

   ```cmd
   docker pull wentaoyang/emis-backend:latest
   ```

2. run docker

   ```cmd
   docker run -d -p 4123:80 wentaoyang/emis-backend:latest
   ```

