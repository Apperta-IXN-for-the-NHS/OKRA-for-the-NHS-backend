# Emis Backend

This is the backend of the Emis project.

## REST APIs

### Get an article by ID

GET {emis-backend}/articles/{articleId}

**JSON return**

```json
{
  "id": "string",
  "title": "string",
  "author": "string",
  "created": "string",
  "body": "string",
  "related": "string[]"
}
```

### Get articles sorted by date (descending order)

GET {emis-backend}/articles\[?limit=10\]\[&start=20\]

Optional parameters:

- limit: the number of shown articles
- start: the start index

**JSON return**

```json
[
  {
    "id": "string",
    "title": "string", 
    "author": "string",
    "created": "string: 2020-08-01"
  }
]
```

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
   docker run -d -p 80:80 emis-backend
   ```


### Pull from Docker Hub

1. pull the docker files

   ```cmd
   docker pull wentaoyang/emis-backend:latest
   ```

2. run docker

   ```cmd
   docker run -d -p 80:80 wentaoyang/emis-backend:latest
   ```

   