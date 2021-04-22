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
    Content-Length: 261
    Content-Type: application/json
    Date: Thu, 22 Apr 2021 12:12:15 GMT
    Server: Werkzeug/0.15.5 Python/3.9.2

    {
        "actors": [
            {
                "age": 10,
                "gender": "male",
                "movies": [
                    {
                        "release_date": "Thu, 22 Apr 2021 13:40:01 GMT",
                        "title": "sometitle"
                    }
                ],
                "name": "somenmae"
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
    Content-Length: 39
    Content-Type: application/json
    Date: Thu, 22 Apr 2021 20:53:09 GMT
    Server: Werkzeug/0.15.5 Python/3.9.2

    {
        "movies": [],
        "success": true
    }
    ```

# Testing Instructions
To run the tests:
```bash
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency
python3 test_app.py
```