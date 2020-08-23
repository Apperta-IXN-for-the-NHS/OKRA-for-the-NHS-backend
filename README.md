# Emis Backend

This is the backend of the Emis project.

## REST APIs

VPS IP Address: 162.62.53.126

Port: 4123

### Get an article by ID

GET 162.62.53.126:4123/articles/{articleId}

**JSON return**

An example:

```json
{
    "id": "string",
    "title": "string",
    "author": "string",
    "created": "string",
    "body": "string",
    "related": [
        {
            "id": "string",
            "title": "string",
            "author": "string",
            "created": "string",
            "view_count": 0
        }
    ]
}
```

### Get articles sorted by trending and similarity

GET 162.62.53.126:4123/articles\[?limit=10\]\[&start=20\]\[&query=keyword]

Optional parameters:

- limit: the number of shown articles
- start: the start index
- query: search term

**JSON return**

An example:

```json
[
  {
    "id": "string",
    "title": "string", 
    "author": "string",
    "created": "2020-08-01"
  }
]
```
## Tests

### Performance Testing
Performance Testing is done by Locust.

1. Go to tests/locust dir

   ```cmd
   cd tests/locust
   ```

2. Run Locust

   ```cmd
   locust
   ```

3. visit http://127.0.0.1:8089/

## Docker

If you want to use the backend locally, first make sure Docker is installed locally

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

   