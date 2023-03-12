#!/usr/bin/env python3
"""SessionDBAuth class"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """create and store a new instance of UserSession
        Return:
            - session id
        """
        if user_id is None:
            return None
        id = super().create_session(user_id)
        if id:
            kwargs = {'user_id': user_id, 'session_id': id}
            user_session = UserSession(**kwargs)
            self.user_id_by_session_id[id] = user_session
            user_session.save()
            UserSession.save_to_file()
            return id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        Return:
            - user id based on session_id
        """
        if session_id is None:
            return None
        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions is None:
            return None
        user_session = user_sessions[0]
        expired_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if expired_time < datetime.now():
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy the UserSession based on session id from cookie
        """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        user_sessions = UserSession.search({'session_id': session_id})
        if user_sessions is None:
            return None
        user_session = user_sessions[0]
        user_session.remove()
        UserSession.save_to_file()
