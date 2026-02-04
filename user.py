# --- USER HIERARCHY ---
import logic

class User:
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

    def change_mail(self, new_mail):
        self._mail = new_mail

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

class Student(User):
    def __init__(self, user_id, mail, pwd):
        super().__init__(user_id, mail, pwd)
        # Private attributes (-)
        self.__usertype = "student"
        self.__degree = ""
        self.__grade = 0.0
        self.__lang = {}
        self.__continents = []
        self.__preferences = []

    def login_retrieve_info(self, user_id):
        pass

    def new_student(self, user_id, mail, pwd):
        new_user_id = "U" + logic.Utilities.generate_random_id()
        
        print(new_user_id)
        pass

    def get_stud_att(self, attribute: str):
        return getattr(self, f"_Student__{attribute}", None)