#!/usr/bin/env python3
"""Session Authentication"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        if user_id is None or type(user_id) is not str:
            return None
        id = str(uuid4())
        self.user_id_by_session_id[id] = user_id
        return id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a User ID based on a Session ID"""
        if session_id is None or type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on cookie value"""
        cookie_val = self.session_cookie(request)
        if cookie_val:
            user_id = self.user_id_for_session_id(cookie_val)
            if user_id:
                user = User.get(user_id)
                if user:
                    return user

    def destroy_session(self, request=None):
        """Deletes the user session/logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id:
            try:
                del self.user_id_by_session_id[session_id]
                return True
            except Exception:
                pass
        return False
