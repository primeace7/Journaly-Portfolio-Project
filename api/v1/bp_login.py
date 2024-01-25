#!/usr/bin/env python3
"""Implementation of login utility the journaly app"""

from flask import request, url_for, g, session, Blueprint, redirect
from werkzeug.security import check_password_hash
from .utilities import fetch_user

login_handler = Blueprint('login_handler', __name__, url_prefix='/login')

@login_handler.route('', methods=['POST'], strict_slashes=False)
def login():
    """return the login view or the journals area
    depending on the rquest type"""
    if request.method == 'POST':
        data = request.json
#        data = request.form
        username_email = data['username']
        password = data['password']
        error = None

        user = fetch_user(username_email) #fetch the user from database
        if not user:
            error = {'Error': 'Invalid username or email'}, 401
            return error
        elif not check_password_hash(user.password, password):
            error = {'Error': 'Invalid password'}, 401
            return error

        if not error:
            session.clear()
            session['user_id'] = getattr(user, 'id')
            return {'success': 'ok'}

        return {'Error': 'There was an error'}, 405
