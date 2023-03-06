#!/usr/bin/env python3
"""Authentication class"""
from flask import request
from typing import List, TypeVar
from models.user import User


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
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path not in excluded_paths:
            aList.append(path + '/')
            for path in aList:
                if path not in excluded_paths:
                    return True
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None
