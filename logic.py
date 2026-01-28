# logic.py
# This code defines all the classes and methods for the logic layer of the application.
# For the moment, the implementation is very minimal, and the only functional class is Utilities.
# In the future, different classes will be contained in different files, and more methods will be implemented.

import pandas as pd
import random

# This class represents the location of a university, encapsulating city, country, continent, and coordinates. We still have to discuss whether we merge it with the University class or keep it separate.
class Location:
    def __init__(self, city, country, continent, coords):
        # Private attributes (-) 
        self.__city = city
        self.__country = country
        self.__continent = continent
        self.__coords = coords # list: [lat, lon]

    # Public method (+) to interact with map libraries
    def gen_map(self, coords_list: list):
        print(f"Generating map for coordinates: {coords_list}")

# This class represents a university with various attributes and methods. 
class University:
    def __init__(self, uni_id, name, degree, grade, lang, cutoff, url, logo, loc_obj):
        # Private attributes (-)
        self.__id = uni_id
        self.__name = name
        self.__degree = degree # list of strings
        self.__grade = float(grade)
        self.__lang = lang # dictionary of requirements
        self.__cutoff_grade = float(cutoff)
        self.__website_url = url
        self.__logo_path = logo
        self.__location = loc_obj # Instance of Location class

    # Public method (+) to safely access private attributes
    def get_uni_att(self, attribute: str):
        """Returns the value of the requested attribute if it exists, else None."""
        pass

# This class defines a generic user with basic attributes and methods for authentication and profile management.
class User:
    def __init__(self, user_id, mail, pwd):
        # Protected attributes (#) for inheritance
        self._ID = user_id
        self._mail = mail
        self._pwd = pwd

    def create_user(self, user_id, mail, pwd):
        """Creates a new user with the given credentials."""
        pass

    def verify_credentials(self, email, pwd):
        """Verifies if the provided email and password match the user's credentials."""
        return self._mail == email and self._pwd == pwd

    # This function will have to ensure in some way that all persistant information is correctly saved on the different csv files.
    def logout(self):
        """Logs out the current user."""
        print(f"User {self._mail} logged out.")

    def change_pwd(self, user_id, new_pwd):
        """Changes the password of a user."""
        self._pwd = new_pwd

    def change_mail(self, new_mail):
        """Changes the email of a user."""
        self._mail = new_mail


# This class represents an admin user with elevated privileges to manage universities, it inherits from User.
class Admin(User):
    def __init__(self, user_id, mail, pwd):
        super().__init__(user_id, mail, pwd)
        # Private attribute (-)
        self.__usertype = "admin"

    # We will possibly deprecate these methods, as we introduced MobilityManager for data handling.
    def login_retrieve_info(self, user_id): pass
    def add_university(self): pass
    def edit_university(self): pass
    def delete_university(self): pass

# This class represents a student user with specific attributes and methods, it inherits from User.
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
        """Retrieves student information upon login. Mainly preferences."""
        pass

    def new_student(self, user_id, mail, pwd):
        """Logs the creation of a new student, updates the users.csv file. """
        pass

    def get_stud_att(self, attribute: str):
        """Returns the value of the requested attribute if it exists, else None."""
        pass

# This class is responsible for scoring and ranking universities based on student profiles.
class ScoringEngine:
    def __init__(self):
        # Private attribute (-)
        self.__ranking = []

    def affinity_score(self, student_obj, university_obj) -> float:
        # Complex calculation logic goes here
        return 0.0

    def risk_score(self, student_obj, university_obj) -> float:
        # Comparison between student grade and university cutoff
        return 0.0

    def rank(self) -> tuple:
        """Returns a list of tuples with both the risk_score and the overall ranking of each university"""
        return ()
    
# This class provides utility functions for data loading, ID generation, PDF creation, and email sending.
class Utilities:
    # Public methods (+)
    
    # We decided to try and use @staticmethods, as these methods do not require any instance-specific data.
    # In the case of Utility funcions, we won't need to create an instance of Utilities to use them.
    @staticmethod
    def load_data(file_path: str):
        """Uses Pandas to load university data efficiently"""
        # Could be eliminated as we added MobilityManager for data handling.
        pass

    @staticmethod
    def generate_random_id() -> str:
        """Generates a random 14-character ID as a string."""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        # Compact form of generating a random string from the specified characters
        # The probability of collision is very low for our use case, thus we won't check for duplicates here.
        return ''.join(random.choice(chars) for _ in range(14))

    @staticmethod
    def choose_random_id(): pass
    
    @staticmethod
    def create_pdf(): pass
    
    @staticmethod
    def send_mail(): pass