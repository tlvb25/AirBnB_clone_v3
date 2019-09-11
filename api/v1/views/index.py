#!/usr/bin/python3
""" index file"""
from api.v1.views import app_views 
from flask import jsonify

if __name__ == "__main__":
    @app_views.route('/status')
    def j_string():
        """ returns the json string status ok"""
        return jsonify({"status": "OK"})
