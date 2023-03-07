#!/usr/bin/env python3
"""Basic authentication"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic authentication"""

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """returns Base64 part of Authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header.startswith('Basic '):
            return authorization_header[6:]
            # else:
            # return None
