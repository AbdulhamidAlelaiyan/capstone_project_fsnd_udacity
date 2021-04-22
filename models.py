import os
from sqlalchemy import Column, String, create_engine, Integer, DateTime, ForeignKey
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Movie
Have title and release data
'''
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=False)

    def  __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        actors = MovieActor.query.filter_by(movie_id=self.id).all()
        actors_formatted = [actor.format() for actor in actors]
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': actors_formatted,
        }

'''
Actors
Have title and release data
'''
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def  __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        movies = MovieActor.query.filter_by(actor_id=self.id).all()
        movies_formatted = [movie.format() for movie in movies]
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': movies_formatted,
        }

'''
MovieActor
Intermediary table that links actors table to movies table (many to many relationships, actors can act in many movies and movies can have many actors)
'''
class MovieActor(db.Model):
    __tablename__ = 'movie_actor'

    actor_id = Column(
        Integer,
        ForeignKey('actors.id'),
        primary_key=True
    )

    movie_id = Column(
        Integer,
        ForeignKey('movies.id'),
        primary_key=True
    )

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()