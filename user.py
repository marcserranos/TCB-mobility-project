import pandas as pd
import random

class User():
    def __init__(self, user_id, mail, pwd):
        # Protected attributes (#) for inheritance
        self._ID = user_id
        self._mail = mail
        self._pwd = pwd

    def create_user(self, user_id, mail, pwd):
        pass

    def verify_credentials(self, email, pwd):
        return self._mail == email and self._pwd == pwd

    def logout(self):
        print(f"User {self._mail} logged out.")

    def change_pwd(self, user_id, new_pwd):
        self._pwd = new_pwd