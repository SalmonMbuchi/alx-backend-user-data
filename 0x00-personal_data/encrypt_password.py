#!/usr/bin/env python3
"""Encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """encrypt a password"""
    passwd = password.encode('utf-8')
    hashed = bcrypt.hashpw(passwd, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Determine if password matches hashed password"""
    passwd = password.encode('utf-8')
    res = bcrypt.checkpw(passwd, hashed_password)
    return res
