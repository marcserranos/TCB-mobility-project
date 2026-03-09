# Admin.py
# This module defines the Admin subclass.

from user import User

class Admin(User):
    def __init__(self, user_id, mail, pwd):
        super().__init__(user_id, mail, pwd)
        # Private attribute (-)
        self.__usertype = "admin"

    def login_retrieve_info(self, user_id):
        pass

    def add_university(self): 
        pass

    def edit_university(self): 
        pass

    def delete_university(self): 
        pass