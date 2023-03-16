#!/usr/bin/env python3
"""
Flask app
"""
# from auth import Auth
from flask import (Flask, abort, jsonify, redirect, request, url_for)

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """
    Return: a JSON payload
    """
    return jsonify({'message': 'Bienvenue'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
