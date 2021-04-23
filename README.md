# Casting Agency App
Application that helps agencies to assign actors to movies.

# Database Model
![Database Diagram](https://i.ibb.co/KsNHmPw/Screen-Shot-2021-04-22-at-11-33-02-AM.png)

# Installation Instructions
```bash
pip3 install -r requirements.txt
export DATABASE_URL="postgresql://[user]:[pass]@[addr]:[port]/[db_name]"
python3 manage.py db init
python3 manage.py db upgrade
python3 app.py
```

# Roles
## Casting Assistant
* Can view actors and movies
## Casting Director
All permissions a Casting Assistant has and:
* Add or delete an actor from the database
* Modify actors or movies
## Executive Producer
All permissions a Casting Director has and:
* Add or delete a movie from the database

# TODOs
* Models
    - [x] Movies with attributes title and release date
    - [x] Actors with attributes name, age and gender
    - [x] Intemediary Table for movies and actors many-to-many relationship
* Endpoints
    - [x] GET /actors
        - [x] Documentation
        - [x] Testing
        - [x] Implementation
    - [x] GET /movies
        - [x] Documentation
        - [x] Testing
        - [x] Implementation
    - [ ] GET /actors/:id
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
    - [ ] GET /movies/:id
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
    - [ ] POST /actors
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
    - [ ] POST /movies
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
    - [ ] PATCH /actors/:id
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
    - [ ] PATCH /movies/:id
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
    - [ ] DELETE /actors/:id
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
    - [ ] DELETE /movies/:id
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
* Roles
    - [x] Casting Assistant
    - [x] Casting Director
    - [x] Executive Producer

# API Documentation

Note: all http request in the documentation was done thourgh cli tool called httpie, for more information please visit [httpie website](https://httpie.io/).
## GET /actors
- Returns all actors and their movies
- Request Arguments: None
- Returns: HTTP Status code 200
- Sample: 
    ```bash
    http GET 127.0.0.1:8080/actors  'Authorization: Bearer ${TOKEN}'
    ```
- Response: 
    ```json
    HTTP/1.0 200 OK
    Access-Control-Allow-Origin: *
    Content-Length: 743
    Content-Type: application/json
    Date: Thu, 22 Apr 2021 21:40:23 GMT
    Server: Werkzeug/0.15.5 Python/3.9.2

    {
        "actors": [
            {
                "age": 21,
                "gender": "male",
                "movies": [
                    {
                        "release_date": "Fri, 23 Apr 2021 00:34:43 GMT",
                        "title": "random movie 1"
                    },
                    {
                        "release_date": "Fri, 23 Apr 2021 00:34:43 GMT",
                        "title": "random movie 2"
                    }
                ],
                "name": "random actor  1"
            },
            {
                "age": 30,
                "gender": "female",
                "movies": [
                    {
                        "release_date": "Fri, 23 Apr 2021 00:34:43 GMT",
                        "title": "random movie 1"
                    },
                    {
                        "release_date": "Fri, 23 Apr 2021 00:34:43 GMT",
                        "title": "random movie 2"
                    }
                ],
                "name": "random actor 2"
            }
        ],
        "success": true
    }
    ```
## GET /movies
- Returns all movies and their actors
- Request Arguments: None
- Returns: HTTP Status code 200
- Sample: 
    ```bash
    http GET 127.0.0.1:8080/movies  'Authorization: Bearer ${TOKEN}'
    ```
- Response: 
    ```json
    HTTP/1.0 200 OK
    Access-Control-Allow-Origin: *
    Content-Length: 734
    Content-Type: application/json
    Date: Thu, 22 Apr 2021 21:41:08 GMT
    Server: Werkzeug/0.15.5 Python/3.9.2

    {
        "movies": [
            {
                "actors": [
                    {
                        "age": 21,
                        "gender": "male",
                        "name": "random actor  1"
                    },
                    {
                        "age": 30,
                        "gender": "female",
                        "name": "random actor 2"
                    }
                ],
                "release_date": "Fri, 23 Apr 2021 00:34:43 GMT",
                "title": "random movie 1"
            },
            {
                "actors": [
                    {
                        "age": 21,
                        "gender": "male",
                        "name": "random actor  1"
                    },
                    {
                        "age": 30,
                        "gender": "female",
                        "name": "random actor 2"
                    }
                ],
                "release_date": "Fri, 23 Apr 2021 00:34:43 GMT",
                "title": "random movie 2"
            }
        ],
        "success": true
    }
    ```
## GET /actors/:id
- Returns actor by id
- Request Arguments: None
- Returns: HTTP Status code 200
- Sample: 
    ```bash
    http GET 127.0.0.1:8080/actors/1  'Authorization: Bearer ${TOKEN}'
    ```
- Response: 
    ```json
    HTTP/1.0 200 OK
    Access-Control-Allow-Origin: *
    Content-Length: 352
    Content-Type: application/json
    Date: Fri, 23 Apr 2021 10:25:39 GMT
    Server: Werkzeug/0.15.5 Python/3.9.2

    {
        "actor": {
            "age": 21,
            "gender": "male",
            "movies": [
                {
                    "release_date": "Fri, 23 Apr 2021 00:34:43 GMT",
                    "title": "random movie 1"
                },
                {
                    "release_date": "Fri, 23 Apr 2021 00:34:43 GMT",
                    "title": "random movie 2"
                }
            ],
            "name": "random actor  1"
        },
        "success": true
    }
    ```

# Testing Instructions
To run the tests:
```bash
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency
psql casting_agency_test < casting_agency_data.dump
python3 test_app.py
```