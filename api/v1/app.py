#!/usr/bin/python3
""" app for task 4"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """teardown flask app"""
    storage.close()


@app.errorhandler(404)
@cross_origin()
def error_handler():
    """error handler"""
    error = {"error": "Not found"}
    return jsonify(error)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or '0.0.0.0'
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True)
