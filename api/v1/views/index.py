#!/usr/bin/python3
""" index file"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def j_status():
    """ returns the json string status ok"""
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats')
def j_stats():
    """ returns the json string stats ok"""
    stats_dict = {"amenities": storage.count("Amenity"),
                  "cities": storage.count("City"),
                  "places": storage.count("Place"),
                  "reviews": storage.count("Review"),
                  "states": storage.count("State"),
                  "users": storage.count("User")}
    return jsonify(stats_dict)
