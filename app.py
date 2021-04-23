import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Movie, Actor, MovieActor, setup_db
from auth import requires_auth


def create_app(test_config=None):
  app = Flask(__name__)
  CORS(app)
  setup_db(app)
  '''
    App routes
  '''

  @app.route('/')
  def check_health():
    return jsonify({
      "success": True,
      "message": "Server working fine"
    })

  @app.route('/actors')
  @requires_auth('read:actors')
  def get_all_actor(*args, **kwargs):
    actors = Actor.query.all()
    actors_formatted = [actor.format() for actor in actors]
    return jsonify({
      'actors': actors_formatted,
      'success': True
    })

  @app.route('/movies')
  @requires_auth('read:movies')
  def get_all_movies(*args, **kwargs):
    movies = Movie.query.all()
    movies_formatted = [movie.format() for movie in movies]
    return jsonify({
      'movies': movies_formatted,
      'success': True
    })

  @app.route('/actors/<id>')
  @requires_auth('read:actors')
  def get_actor(*args, **kwargs):
    try:
      actor = Actor.query.filter_by(id=kwargs['id']).all()[0]
      return jsonify({
        'success': True,
        'actor': actor.format(),
      })
    except:
      return abort(404)

  @app.route('/movies/<id>')
  @requires_auth('read:movies')
  def get_movie(*args, **kwargs):
    try:
      actor = Movie.query.filter_by(id=kwargs['id']).all()[0]
      return jsonify({
        'success': True,
        'movie': actor.format(),
      })
    except:
      return abort(404)

  @app.route('/actors', methods=['POST'])
  @requires_auth('create:actors')
  def create_actor(*args, **kwargs):
    try:
      data = request.get_json()
      new_actor = Actor(name=data['name'], age=data['age']
        , gender=data['gender'])
      new_actor.insert()

      return jsonify({
        'success': True,
        'actor': data
      }), 201
    except Exception as e:
      print(e)
      return abort(400)


  @app.route('/movies', methods=['POST'])
  @requires_auth('create:movies')
  def create_movie(*args, **kwargs):
    # try:
    #   data = request.get_json()
    #   new_movie = Movie(title=data['title'], release_date=data['release_date'])
    #   new_movie.insert()
      
    #   return jsonify({
    #     'success': True,
    #     'movie': data
    #   }), 201
    # except:
    #   return abort(400)
    return "Not implemented 'yet'!"

  @app.route('/actors/<id>', methods=['PATCH'])
  def update_actor(*args, **kwargs):
    return "Not implemented 'yet'!"

  @app.route('/movies/<id>', methods=['PATCH'])
  def update_movie(*args, **kwargs):
    return "Not implemented 'yet'!"

  @app.route('/actors/<id>', methods=['DELETE'])
  def delete_actor(*args, **kwargs):
    return "Not implemented 'yet'!"

  @app.route('/movies/<id>', methods=['DELETE'])
  def delete_movie(*args, **kwargs):
    return "Not implemented 'yet'!"

  '''
  Error Handlers based on HTTP status codes
  '''
  @app.errorhandler(400)
  def unauthenticated_access(error):
    return (
        jsonify(
            {"success": False, "error": 400, "message": "bad request"}
        ),
        400,
    )

  @app.errorhandler(401)
  def unauthenticated_access(error):
    return (
        jsonify(
            {"success": False, "error": 401, "message": "user unauthenticated"}
        ),
        401,
    )


  @app.errorhandler(403)
  def unauthorized_access(error):
      return (
          jsonify(
              {"success": False, "error": 403, "message": "user unauthorized"}
          ),
          403,
      )

  @app.errorhandler(404)
  def not_found(error):
      return (
          jsonify(
              {"success": False, "error": 404, "message": "resource not found"}
          ),
          404,
      )


  @app.errorhandler(422)
  def unprocessable(error):
      return (
          jsonify({"success": False, "error": 422, "message": "unprocessable"}),
          422,
      )


  @app.errorhandler(500)
  def unprocessable(error):
      return (
          jsonify(
              {
                  "success": False,
                  "error": 500,
                  "message": "internal server error",
              }
          ),
          500,
      )


  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)