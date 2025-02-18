#!/usr/bin/python3
"""Module creates the Flask app, app_views
"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def api_status():
    """Method creates a JSON payload when called
    """
    response = {'status': "OK"}
    return jsonify(response)