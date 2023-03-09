#!/usr/bin/env python3
"""Expiration"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """adds expiration date to a session ID"""
    def __init__(self):
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a session id"""
        id = super().create_session(user_id)
        if id:
            self.user_id_by_session_id[id] = {'user_id': user_id, 'created_at': datetime.now()}
            return id
        return None

    def user_id_for_session_id(self, session_id=None):
        """retrieve a user id using a session id"""
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict:
            if self.session_duration <= 0:
                return session_dict.get('user_id')
            if session_dict.get('created_at') is None:
                return None
            current_time = session_dict.get('created_at') + self.session_duration
            if current_time > timedelta():
                return None
            return session_dict.get('user_id')
        return None
