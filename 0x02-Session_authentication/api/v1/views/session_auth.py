#!/usr/bin/env python3
"""Handle all routes for Session authentication"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST /auth_session/login
    Return:
        - authenticated user"""
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({'error': 'email missing'}), 400
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({'error': 'password missing'}), 400
    users = User.search({'email': email})
    if users is None or users == []:
        return jsonify({'error': 'no user found for this email'}), 404
    for u in users:
        if u.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(u.id)
            user = jsonify(u.to_json())
            user.set_cookie(getenv('SESSION_NAME'), session_id)
            return user
        return jsonify({'error': 'wrong password'}), 401


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """
    DELETE /api/v1/auth_session/logout
    Return:
        - Empty dictionary, status code 200
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
