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
        self.database_path = "postgresql://postgres@localhost:5432/casting_agency_test"
        setup_db(self.app, self.database_path)

        # Setting the tokens for authentication and authorization
        self.tokens = {
            'casting_assistant': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY2WXV5dU81eDZscWMzV0xGcWl5RSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODE0NzM2MTMwYzY1MDA3MGQ5YjYzZiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTkxNzI4NjksImV4cCI6MTYxOTI1OTI2OSwiYXpwIjoiTTluZkVlSGxpeWxHMk11N0pmSFNoNGJsQlIzTnFZdU8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.WI9nT1RbagI1M7po0kVLKr2_97ELRWEdjKBZj_mI40_c5Chpomq9oMSbQ0Zau6OmQeEHmZyIYcK1p2_HdnEyfiYfxGoH_S3KDVVmiWgMdfCcbGq4ypUqGPt4Y6GxXE5bloleh2QqQvLtoYVgq16n_QwZauH-ovjOKaArvD0ZcIjLdeOBJnXAiQOM4znHC5yf5Ec_GefUZzsNwae2p8_by_0YcyMHuR4StHClt6-6wddKiEA0cq0kGl9dB8aNSU89WPsR5O4V2NoGvu__t20SmXwWCCtSOKgFW-fcnYTCZT6LofwZZZ5EFwdYnaC6EJBO9GKzwULXHklDiVSUEReUFA',
            'casting director': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY2WXV5dU81eDZscWMzV0xGcWl5RSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODE0NzY3OGJiYzM4MDA2OTc5MDE3NSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTkxNzI4MzEsImV4cCI6MTYxOTI1OTIzMSwiYXpwIjoiTTluZkVlSGxpeWxHMk11N0pmSFNoNGJsQlIzTnFZdU8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.E3tOaOqAr-IFjhFnt57OIFPUbIDcnPpZ5M8RSuGSP-ja-LcCm62lVtpo4CNeJCO4Y85NE3i_bnYr2yLPOR3z0Sp4jYqOSWh1jxFretH6lpiEMczLetvhR8TXefejiZRTEZbypBV-FixzTz9Ctn3ighKjvQMCG802OYQ0mtO34YgMWjwkfADC0UM-46kY5dspq1NSwQGujTu2SCAQHmvCwDPN7GM4xD7TAjCkjdDcOb2409YY0_mhRpp_9UhPIU7hneNzqFJcsta0LFFqk_o_NogQn6nRHmZsPeYCgg3W-Sn_DZ0ldNn5RnbzQhK0BlTC0WLOwA42mENNohBp3TpVpA',
            'executive producer': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY2WXV5dU81eDZscWMzV0xGcWl5RSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODE0Nzk3Y2YyODAxMDA3MmNjZTZkYSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTkxNzI3NzMsImV4cCI6MTYxOTI1OTE3MywiYXpwIjoiTTluZkVlSGxpeWxHMk11N0pmSFNoNGJsQlIzTnFZdU8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.SKePVMUoN-6SVDEVBig36YfNXAfbaY67iY9YEzO_x8cntgdvhSKS6nGxT6J0kGlRrTFbjf0pY_nTwCNd_TAa2Kv7DVmYMp_y0Of4tKZZrjVyrJc9qpiCSa5K_95Q9on4EJqDGFJje9h5JBucwbLVvVvLPmbq62FXJIjwttA3fty2pqqeIxOXHef_kn6EM91b6Xr-eo5XDNZpylL7Z8CnDjFPFk9EfkmH3VGbGxhCxMLLmhflldSfiIIpF8LoMnKUS-P1k2MRw8kUCNAFSXT4DmsR5C021I0lar6dk6gOmaFGEmeYwt1nLB7g-fYI8lpAqX1we9ejmlXHH-1tV0mw7A'
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

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()