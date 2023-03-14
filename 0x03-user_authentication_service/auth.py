#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    Hash a password
    """
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Hash the password, save user to database
        Return:
            - User object
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email, hashed.decode('utf-8'))

#     def valid_login(self, email: str, password: str) -> bool:
#         """
#         Validate user credentials
#         """
#         try:
#             user = self._db.find_user_by(email=email)
#             encoded = password.encode('utf-8')
#             return bcrypt.checkpw(encoded,
#                                   user.hashed_password.encode('utf-8'))
#         except NoResultFound:
#             return False

#     def _generate_uuid(self) -> str:
#         """
#         Return:
#             - string representation of UUID
#         """
#         return str(uuid4())

#     def create_session(self, email: str) -> str:
#         """
#         Finds the user via email, generates a UUID and
#         stores it as the user's session id
#         """
#         try:
#             user = self._db.find_user_by(email=email)
#             session_id = self._generate_uuid()
#             self._db.update_user(user.id, session_id=session_id)
#             return session_id
#         except NoResultFound:
#             return None

#     def get_user_from_session_id(self, session_id: str) -> User | None:
#         """
#         Finds user by session id
#         """
#         if session_id is None:
#             return None
#         try:
#             user = self._db.find_user_by(session_id=session_id)
#             return user
#         except NoResultFound:
#             return None

#     def destroy_session(self, user_id: int) -> None:
#         """
#         Destroys a session
#         """
#         try:
#             user = self._db.find_user_by(id=user_id)
#             self._db.update_user(user_id, session_id=None)
#         except NoResultFound:
#             return None
