# University.py
# This class represents a university, encapsulating all relevant information such as name, degree requirements, grade requirements, language requirements, cutoff grade, website URL, logo path, and location.

from location import Location

class University:
    def __init__(self, uni_id, name, degree, grade, lang, lang_levels, cutoff, url, logo, loc_obj,
                 ranking=None, weather=None, nightlife=None, cost=None, spots=None):
        self.__id = uni_id
        self.__name = name
        self.__degree = degree  # list of strings (acceptable degrees)
        self.__grade = float(grade)
        # languages required by the university; the CSV stores a semicolon-separated
        # string which the Catalog will parse into a list.
        self.__lang = lang
        # dictionary mapping language name to required level (e.g. {'English':'B2'})
        self.__lang_levels = lang_levels or {}
        self.__cutoff_grade = float(cutoff)
        self.__website_url = url
        self.__logo_path = logo
        self.__location = loc_obj  # instance of Location class
        # preference-related values that are used by the scoring engine
        self.__ranking = ranking
        self.__weather = weather
        self.__nightlife = nightlife
        self.__cost_of_living = cost
        self.__spots = spots

    def get_uni_att(self, attribute: str):
        """Returns the value of the requested attribute if it exists, else None."""
        return getattr(self, f"_{self.__class__.__name__}__{attribute}", None)

    def get_logo_path(self) -> str:
        """Returns the full path to the university logo image."""
        uni_id = self.get_uni_att('id')
        if uni_id:
            return f"images/{uni_id}.png" # construct the path based on the university ID
        return ""

    def to_dict(self) -> dict:
        """Dict representation for GUI tables or exports."""
        
        return {
            "id": self.__id,
            "name": self.__name,
            "degree": self.__degree,
            "grade": self.__grade,
            "lang": self.__lang,
            "cutoff_grade": self.__cutoff_grade,
            "website_url": self.__website_url,
            "logo_path": self.__logo_path,
            "location": {
                "city": self.__location.get_city() if self.__location else None,
                "country": self.__location.get_country() if self.__location else None,
                "continent": self.__location.get_continent() if self.__location else None,
                "coords": self.__location._Location__coords if self.__location else None,
            },
            # preference-related values use the same labels the student
            # preferences list contains so comparison later is natural.
            "Academic Rank": self.__ranking,
            "Weather": self.__weather,
            "Nightlife": self.__nightlife,
            "Cost of Living": self.__cost_of_living,
        }
