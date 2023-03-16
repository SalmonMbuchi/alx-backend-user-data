#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password
    """
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, bcrypt.gensalt())
