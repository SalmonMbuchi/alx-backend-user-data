#!/usr/bin/env python3
"""Authentication class"""
from flask import request
from typing import List, TypeVar
from models.user import User
from os import getenv


SESSION_NAME = '_my_session_id'

class Auth:
    """Authentication class that will serve as a template
    for all authentication systems to be implemented"""

    def __init__(self):
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns True if the path is not in excluded_paths"""
        aList = []
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns value of header key: Authorization"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(SESSION_NAME)
