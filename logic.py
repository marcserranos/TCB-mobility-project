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
        return getattr(self, f"_{self.__class__.__name__}__{attribute}", None)

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
    
