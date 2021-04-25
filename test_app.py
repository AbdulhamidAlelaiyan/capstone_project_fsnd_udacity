import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor, MovieActor


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('TEST_DATABASE_URL')
        setup_db(self.app, self.database_path)

        # Setting the tokens for authentication and authorization
        self.tokens = {
            'casting_assistant':
            f'Bearer {os.environ.get("jwt_casting_assistant")}',
            'casting_director':
            f'Bearer {os.environ.get("jwt_casting_director")}',
            'executive_producer':
            f'Bearer {os.environ.get("jwt_executive_producer")}',
        }
        # Setting the default headers
        self.headers = {
            'Content-Type': 'application/json',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def test_authenticated_get_actors(self):
        self.headers['Authorization'] = self.tokens['casting_assistant']

        response = self.client().get('/actors', headers=self.headers)
        data = json.loads(response.data)

        self.assertTrue(data['actors'])

    def test_unauthenticated_get_actors(self):
        response = self.client().get('/actors', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(data['error'], 401)

    def test_authenticated_get_movies(self):
        self.headers['Authorization'] = self.tokens['casting_assistant']

        response = self.client().get('/movies', headers=self.headers)
        data = json.loads(response.data)

        self.assertTrue(data['movies'])

    def test_unauthenticated_get_movies(self):
        response = self.client().get('/movies', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(data['error'], 401)

    def test_authenticated_get_actor_by_id(self):
        self.headers['Authorization'] = self.tokens['casting_assistant']

        response = self.client().get('/actors/1', headers=self.headers)
        data = json.loads(response.data)

        self.assertTrue(data['actor'])

    def test_unauthenticated_get_actor_by_id(self):
        response = self.client().get('/actors/1', headers=self.headers)
        data = json.loads(response.data)

        self.assertTrue(data['error'], 401)

    def test_authenticated_get_movie_by_id(self):
        self.headers['Authorization'] = self.tokens['casting_assistant']

        response = self.client().get('/movies/1', headers=self.headers)
        data = json.loads(response.data)

        self.assertTrue(data['movie'])

    def test_unauthenticated_get_movie_by_id(self):
        response = self.client().get('/movies/1', headers=self.headers)
        data = json.loads(response.data)

        self.assertTrue(data['error'], 401)

    def test_authenticated_create_actor(self):
        actor = {
            "name": "ahmed khalid",
            "age": 20,
            "gender": "male",
        }

        self.headers['Authorization'] = self.tokens['casting_director']
        response = self.client().post('/actors',
                                      json=actor,
                                      headers=self.headers)

        self.assertEqual(response.status_code, 201)

    def test_unauthenticated_create_actor(self):
        actor = {
            "name": "ahmed khalid",
            "age": 20,
            "gender": "male",
        }
        response = self.client().post('/actors',
                                      json=actor,
                                      headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_authenticated_create_movie(self):
        movie = {
            "title": "ahmed khalid",
            "release_date": '2020-10-10',
        }

        self.headers['Authorization'] = self.tokens['executive_producer']
        response = self.client().post('/movies',
                                      json=movie,
                                      headers=self.headers)

        self.assertEqual(response.status_code, 201)

    def test_unauthenticated_create_movie(self):
        movie = {
            "title": "ahmed khalid",
            "release_date": '2020-10-10',
        }
        response = self.client().post('/movies',
                                      json=movie,
                                      headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_authenticated_update_actor(self):
        update_data = {
            "name": "some actor 101",
        }

        self.headers['Authorization'] = self.tokens['executive_producer']
        response = self.client().patch('/actors/1',
                                       json=update_data,
                                       headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_update_actor(self):
        update_data = {
            "name": "some actor 101",
        }

        response = self.client().patch('/actors/1',
                                       json=update_data,
                                       headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_authenticated_update_movie(self):
        update_data = {
            "title": "some title 101",
        }

        self.headers['Authorization'] = self.tokens['executive_producer']
        response = self.client().patch('/movies/1',
                                       json=update_data,
                                       headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_update_movie(self):
        update_data = {
            "name": "some title 101",
        }

        response = self.client().patch('/movies/1',
                                       json=update_data,
                                       headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_authenticated_delete_actor(self):
        self.headers['Authorization'] = self.tokens['executive_producer']
        response = self.client().delete('/actors/3', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_delete_actor(self):
        response = self.client().delete('/actors/3', headers=self.headers)

        self.assertEqual(response.status_code, 401)

    def test_authenticated_delete_movie(self):
        self.headers['Authorization'] = self.tokens['executive_producer']
        response = self.client().delete('/movies/3', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_delete_movie(self):
        response = self.client().delete('/movies/3', headers=self.headers)

        self.assertEqual(response.status_code, 401)

    # RBAC Tests

    # Casting assistant Role
    def test_casting_assistant_unauthorized_delete_movie(self):
        self.headers['Authorization'] = self.tokens['casting_assistant']
        response = self.client().delete('/movies/3', headers=self.headers)

        self.assertEqual(response.status_code, 403)

    def test__casting_assistant_unauthorized_update_movie(self):
        update_data = {
            "title": "some title 101",
        }

        self.headers['Authorization'] = self.tokens['casting_assistant']
        response = self.client().patch('/movies/1',
                                       json=update_data,
                                       headers=self.headers)

        self.assertEqual(response.status_code, 403)

    # Casting director Role
    def test_casting_director_unauthorized_create_movie(self):
        movie = {
            "title": "ahmed khalid",
            "release_date": '2020-10-10',
        }

        self.headers['Authorization'] = self.tokens['casting_director']
        response = self.client().post('/movies',
                                      json=movie,
                                      headers=self.headers)

        self.assertEqual(response.status_code, 403)

    def test_casting_director_unauthorized_delete_movie(self):
        self.headers['Authorization'] = self.tokens['casting_director']
        response = self.client().delete('/movies/3', headers=self.headers)

        self.assertEqual(response.status_code, 403)

    # Executive producer Role
    def test_executive_producer_authorized_create_actor(self):
        actor = {
            "name": "ahmed khalid",
            "age": 20,
            "gender": "male",
        }

        self.headers['Authorization'] = self.tokens['executive_producer']
        response = self.client().post('/actors',
                                      json=actor,
                                      headers=self.headers)

        self.assertEqual(response.status_code, 201)

    def test_executive_producer_authorized_get_actor_by_id(self):
        self.headers['Authorization'] = self.tokens['executive_producer']

        response = self.client().get('/actors/1', headers=self.headers)
        data = json.loads(response.data)

        self.assertTrue(data['actor'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
