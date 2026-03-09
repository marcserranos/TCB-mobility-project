# Location.py
# This class represents the location of a university, encapsulating city, country, continent, and coordinates. We still have to discuss whether we merge it with the University class or keep it separate.

class Location:
    def __init__(self, city, country, continent, coords):
        # Private attributes (-) 
        self.__city = city
        self.__country = country
        self.__continent = continent
        self.__coords = coords # list: [lat, lon]

    # accessors helpful for serialization and filtering
    def get_city(self):
        return self.__city

    def get_country(self):
        return self.__country

    def get_continent(self):
        return self.__continent

    def get_coords(self):
        return self.__coords