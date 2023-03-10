#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """Basic authentication"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """returns Base64 part of Authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Decode base64 string"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None
        try:
            byte = base64.b64decode(base64_authorization_header)
            return byte.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Returns user email and password from Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        split_header = decoded_base64_authorization_header.split(":", 1)
        return (split_header[0], split_header[1])

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instace for a request"""
        header_value = self.authorization_header(request)
        if header_value is not None:
            base64 = self.extract_base64_authorization_header(header_value)
            if base64 is not None:
                decoded = self.decode_base64_authorization_header(base64)
                if decoded is not None:
                    email, passwd = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, passwd)
        return
