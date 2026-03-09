# Admin.py
# This module defines the Admin subclass.

from user import User

class Admin(User):
    def __init__(self, user_id, mail, pwd):
        super().__init__(user_id, mail, pwd)
        # Private attribute (-)
        self.__usertype = "admin"