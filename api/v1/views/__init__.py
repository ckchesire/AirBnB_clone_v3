#!/usr/bin/python3
"""Module creates the Flask app blueprint

   This module is responsible for defining the central Blueprint object that
   organizes a collection of related routes under a common URL prefix.
"""
from flask import Blueprint
from api.v1.views.index import *

app_views = Blueprint('app_views', __name__, url_prefix='api/v1')
