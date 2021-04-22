import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db
from auth import requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  


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