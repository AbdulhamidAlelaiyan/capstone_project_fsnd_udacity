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
            'casting_assistant': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY2WXV5dU81eDZscWMzV0xGcWl5RSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODE0NzM2MTMwYzY1MDA3MGQ5YjYzZiIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTkwODU2NTgsImV4cCI6MTYxOTE3MjA1OCwiYXpwIjoiTTluZkVlSGxpeWxHMk11N0pmSFNoNGJsQlIzTnFZdU8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6YWN0b3JzIiwicmVhZDptb3ZpZXMiXX0.lH91wy5IByLvTRb5C3nkNDFB7DkvIrngdRViS5xqAkiTpNImIB2w861Z8IfO7u6so-ol2d0-JL84nZ3ksQWj9qnXqXFKrJqevouz32-8Ap7jiFi7fo2JDOu92OlfmfxsHn4U7mfq3qr6DHSg-f5Su7sdPiEuNn0zInRQF5LT6BcJhbdMzcj5SSjzYKZMbbw6mY8aX8kYi7fzlCHoa-IsazqoAqatwBwf3n3KeNBzIitnpRmw3LOiBTFRFkQGvWvp8903O0cLXZX_r96YOKT03rz3jC91bAtAuCM2gDhnYR7ckselzrHq2b5mctOQfSIPcgKARYql-qlEKJwDgzQqtA',
            'casting director': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY2WXV5dU81eDZscWMzV0xGcWl5RSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODE0NzY3OGJiYzM4MDA2OTc5MDE3NSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTkwODU1OTcsImV4cCI6MTYxOTE3MTk5NywiYXpwIjoiTTluZkVlSGxpeWxHMk11N0pmSFNoNGJsQlIzTnFZdU8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJkZWxldGU6YWN0b3JzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.fdoXX0JPUPnYWOL564eSEX9fEhhM3Sw5ctNe-oTtNhE932sunbN2BEZQy9u4zUSzUZGF2x1ON0wQuz5s-1E0mmB8Pt7G66EKGHJD51GxlCxd2ZbUf3zPHiJdy9qYSoTYEkI9assOeqmdj8JnHSakul4Vgy5R-QMeuqQn7DTB_dnW6QWDEQ6EbOaaCkNiDxFgkxJEmwh0wlsYZnv-b2L8zYFhCjR7v6uDeqiv_157ytNy7cNc5_uw3ccfEyJZenxCYAI1TzE14PSHvXX3rWv43B3Npr3KYdcKG3nRmbA4Zq9CfWrV4DjoiGRjhKHjqCt0kW_MJvlXzYMUo_TCiAwRyA',
            'executive producer': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImY2WXV5dU81eDZscWMzV0xGcWl5RSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtYWEudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwODE0Nzk3Y2YyODAxMDA3MmNjZTZkYSIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE2MTkwODUzMjAsImV4cCI6MTYxOTE3MTcyMCwiYXpwIjoiTTluZkVlSGxpeWxHMk11N0pmSFNoNGJsQlIzTnFZdU8iLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTphY3RvcnMiLCJjcmVhdGU6bW92aWVzIiwiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.THKyrMftnzKGtiEO_imPDfYQZ3VMEHKflKBNe_JHitwm9u9AnY1iwnXlukO_DEeaoJgdMxR3VV7QAinlwwpgnfkXodr8y4FjVvdZDU3QQbKX4u8Pr7cVT8aBgaoYV7hi6LBt3cmSdKws-8o-PbASM3MSnfn-ZhUU0wMwRvgcH9fInmLM46B2G7vzECyEL1MA5AZl7dN1u7pRSlV4Xka8X0zUMdvjYc9guGlTLz_U7iFCiPpz3K6lirgCPKUWglSuKESyok6LfTg8dKIAJty_HZs62v-K75fTu0n6Q3Zq9zFWlzKPpK8iAYvufHhDnw57CFFswRfrL-oh7jLe_yhLjA'
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
        

    def test_unauthenticated_get_actors(self):
        response = self.client().get('/actors', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(data['error'], 401)

    def test_authenticated_get_actors(self):
        self.headers['Authorization'] = self.tokens['casting_assistant']

        response = self.client().get('/actors', headers=self.headers)
        data = json.loads(response.data)

        self.assertEqual(data['actors'], [])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()