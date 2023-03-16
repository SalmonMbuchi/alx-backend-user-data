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


AUTH = Auth()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
