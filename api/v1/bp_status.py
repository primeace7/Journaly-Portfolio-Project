#!/usr/bin/env python3
"""Implementation a status view for checking the status of the API service"""

from flask import Blueprint

status_handler = Blueprint('app_views', __name__, url_prefix='status')

@status_handler.route('/', strict_slashes=False)
def status():
    """return the status of the API server"""
    return {'status': 'OK'}
