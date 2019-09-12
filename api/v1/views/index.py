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
    stats_dict = {
        "amenities": storage.count("Amenity"), 
        "cities": storage.count("Cities"), 
        "places": storage.count("Places"), 
        "reviews": storage.count("Reviews"), 
        "states": storage.count("States"), 
        "users": storage.count("Users")
    }
    return jsonify(stats_dict)
