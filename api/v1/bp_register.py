#!/usr/bin/env python3
"""Implement the register view handler for new users"""

from flask import Blueprint, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from .utilities import storage

register_handler = Blueprint('register_view', __name__, url_prefix='/register')
@register_handler.route('', methods=['POST'], strict_slashes=False)
def register():
    """The register view-handler"""
    error = None
    data = request.json
#    data = request.form.copy()
    if not data:
        #400 is HTTP status code for bad request
        error = {'Error': 'Invalid data'}, 400
        return error

    if request.method == 'POST' and data:
        username = data['username']
        if not username:
            error = {'Error': 'Username is required'}, 400
            return error
        elif not validate_username(username):
            # 405 is HTTP status code for Method not allowed
            error = {'Error': 'Username is unvavailable'}, 405
            return error

        email = data['email']
        if not email:
            error = {'Error': 'Email is required'}, 400
            return error
        elif not validate_email(email):
            error = {'Error': 'Email is already in use'}, 400
            return error

        password = data['password']
        if not password:
            error = {'Error': 'Password is required'}, 400
            return error

        firstname = data['firstName']
        if not firstname:
            error = {'Error': 'Firstname is required'}, 400
            return error
        del data['firstName']
        data['firstname'] = firstname

        lastname = data.get('lastName')
        if lastname:
            del data['lastName']
            data['lastname'] = lastname

        create_user(data)
        return {'success': 'ok'} #redirect(url_for('app_views.login_handler.login'))

    return {'Error': 'There was an error'}, 400


def create_user(data):
    """create a new user from the provided data and store in database"""
    User = storage.classes.get('User')
    data['password'] = generate_password_hash(data['password'])
    new_user = User(**data)
    storage.add(new_user)
    storage.save()


def validate_username(username):
    """check if a username already exists in the database"""
    from .utilities import storage

    all_users = storage.all('User')
    if len(list(all_users)) != 0:
        all_usernames = [key.username for key in all_users[0].keys()]
    else:
        all_usernames = []

    if username not in all_usernames:
        return True
    return False

def validate_email(email):
    """check if an email already exists in the database"""
    from .utilities import storage

    all_users = storage.all('User')
    if len(list(all_users)) != 0:
        all_emails = [key.email for key in all_users[0].keys()]
    else:
        all_emails = []

    if email not in all_emails:
        return True
    return False
