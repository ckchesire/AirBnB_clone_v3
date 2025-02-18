#!/usr/bin/python3
"""Module creates the Flask app, app_views

   It serves as the entry point for the API's view functions
   by importing the necessary blueprint (app_views) and registering routes.
   The module focuses on defining status endpoint functionality.
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
    """Method creates a JSON payload when called, that returns the API status
    
       Example:
         $ curl -X GET http://localhost:5000/api/v1/status
    """
    response = {'status': "OK"}
    return jsonify(response)
