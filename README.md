# Casting Agency App
Application that helps agencies to assign actors to movies.

# Database Model
![Database Diagram](https://i.ibb.co/KsNHmPw/Screen-Shot-2021-04-22-at-11-33-02-AM.png)

# Installation Instructions
```
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
    - [ ] GET /actors
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
    - [ ] GET /movies
        - [ ] Documentation
        - [ ] Testing
        - [ ] Implementation
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