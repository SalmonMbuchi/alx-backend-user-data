#!/usr/bin/env python3
"""
Flask app
"""
from auth import Auth
from flask import (Flask, abort, jsonify, redirect, request, url_for)

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Return: a JSON payload
    """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """
    user endpoint
    """
    email = request.form.get('email')
    if not email:
        return None
    password = request.form.get('password')
    if not password:
        return None
    try:
        AUTH.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """
    Login a user
    """
    email = request.form.get('email')
    if not email:
        return None
    password = request.form.get('password')
    if not password:
        return None
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        cookie = jsonify({'email': email, 'message': 'logged in'})
        cookie.set_cookie('session_id', session_id)
        return cookie
    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Log out a user
    """
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    user profile
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({'email': user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """
    generates a reset token
    """
    email = request.form.get('email')
    if email is None:
        abort(403)
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({'email': email, 'reset_token': token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Update the password
    """
    email = request.form.get('email')
    if email is None:
        abort(400)
    reset_token = request.form.get('reset_token')
    if reset_token is None:
        abort(400)
    new_password = request.form.get('new_password')
    if new_password is None:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({'email': email, 'message': 'Password updated'}), 200
    except ValueError:
        abort(403)


AUTH = Auth()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
