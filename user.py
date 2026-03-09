# User.py
# This module defines the base User class.

class User:
    def __init__(self, user_id, mail, pwd):
        # Protected attributes (#) for inheritance
        self._ID = user_id
        self._mail = mail
        self._pwd = pwd

    def logout(self):
        pass

