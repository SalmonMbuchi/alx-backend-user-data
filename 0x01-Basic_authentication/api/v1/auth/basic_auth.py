#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth
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
