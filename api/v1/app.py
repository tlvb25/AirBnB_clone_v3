#!/usr/bin/python3
""" app for task 4"""
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(self):
    """teardown flask app"""
    storage.close()

if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    app.run(host=host, port=port, threaded=True)
