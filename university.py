# university.py
# This file contains the University and Location classes.

# This class represents a university, encapsulating all relevant information such as name, degree requirements, grade requirements, language requirements, cutoff grade, website URL, logo path, and location.
class University:
    def __init__(self, uni_id, name, degree, grade, lang, lang_levels, cutoff, url, logo, loc_obj,
                 ranking=None, weather=None, nightlife=None, cost=None):
        # Private attributes (-)
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
        self.__location = loc_obj  # Instance of Location class

        # preference-related values that are used by the scoring engine
        self.__ranking = ranking          # numeric, smaller is better
        self.__weather = weather          # textual description
        self.__nightlife = nightlife      # numeric
        self.__cost_of_living = cost      # numeric

    # Public method (+) to safely access private attributes
    def get_uni_att(self, attribute: str):
        """Returns the value of the requested attribute if it exists, else None."""
        return getattr(self, f"_{self.__class__.__name__}__{attribute}", None)

    def is_eligible(self, student) -> bool:
        """Basic eligibility check used by the catalog filter.

        - student grade must meet or exceed cutoff
        - degree (if both sides have a value) must match
        - continent and language restrictions may also be applied.
        """
        # cutoff
        if student.get_grade() < self.__cutoff_grade:
            return False

        # degree check
        stud_deg = student.get_degree()
        if stud_deg and self.__degree:
            if stud_deg not in self.__degree:
                return False

        # continent check
        cont = None
        if self.__location is not None:
            cont = self.__location.get_continent()
        if cont and student.get_continents():
            if cont not in student.get_continents():
                return False

        # language check: all required languages must appear in student's profile
        req_langs = []
        if isinstance(self.__lang, list):
            req_langs = self.__lang
        elif isinstance(self.__lang, str):
            # sometimes stored as semicolon-separated string
            req_langs = [l.strip() for l in self.__lang.split(";") if l.strip()]

        for l in req_langs:
            if l and l not in student.get_languages():
                return False

        return True

    def to_dict(self) -> dict:
        """Flattenable representation for GUI tables or exports.

        The keys used here mirror the student's preference names where
        appropriate so that inspecting the output side-by-side makes it
        easy to see how the two data structures line up.  For example a
        student's preference list contains strings like "Cost of Living"
        and "Academic Rank"; this representation uses the same labels.
        """
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

    # accessors helpful for serialization and filtering
    def get_city(self):
        return self.__city

    def get_country(self):
        return self.__country

    def get_continent(self):
        return self.__continent

    def get_coords(self):
        return self.__coords


# ---------------------------------------------------------------------------
# container for creating/filtering/ranking University objects
class Catalog:
    def __init__(self, csv_path: str = "data/entries.csv"):
        self._csv = csv_path
        self._universities: list[University] = []

    def load(self) -> None:
        """Load CSV and convert rows into University instances."""
        try:
            import pandas as pd
            df = pd.read_csv(self._csv)
        except FileNotFoundError:
            self._universities = []
            return

        cats: list[University] = []
        for _, row in df.iterrows():
            langs = []
            if 'Languages required' in row and pd.notna(row['Languages required']):
                langs = [l.strip() for l in str(row['Languages required']).split(';') if l.strip()]

            # build language level requirements from individual columns
            lang_levels = {}
            for lang_col in ['English','Spanish','French','German','Italian','Portuguese','Chinese','Japanese']:
                if lang_col in row and pd.notna(row[lang_col]) and str(row[lang_col]).strip() != '':
                    lang_levels[lang_col] = str(row[lang_col]).strip()

            loc = Location(
                city=row.get('City', ''),
                country=row.get('Country', ''),
                continent=row.get('Continent', ''),
                coords=[row.get('Latitude', None), row.get('Longitude', None)]
            )

            u = University(
                uni_id=row.get('ID', ''),
                name=row.get('Name', ''),
                degree=[d.strip() for d in str(row.get('Degree', '')).split(';') if d.strip()] if 'Degree' in row else [],
                grade=row.get('Minimum grade', 0.0),
                lang=langs,
                lang_levels=lang_levels,
                cutoff=row.get('Previous cutoff grade', row.get('Minimum grade', 0.0)),
                url=row.get('Website', ''),
                logo=row.get('Logo', ''),
                loc_obj=loc,
                ranking=row.get('University Ranking', None),
                weather=row.get('Weather', None),
                nightlife=row.get('Nightlife', None),
                cost=row.get('Cost of living', None),
            )
            cats.append(u)

        self._universities = cats

    def all(self) -> list[University]:
        return list(self._universities)

    def filter_for(self, student, engine=None) -> list[University]:
        """Return universities matching student's basic eligibility.

        ``engine`` may be supplied; if provided its ``is_eligible`` method will
        be used instead of the old ``University.is_eligible`` helper.  This
        allows the filtering logic to evolve in the scoring engine while
        keeping legacy support.
        """
        if engine is not None:
            return [u for u in self._universities if engine.is_eligible(student, u)]
        else:
            # fall back to previous behaviour until callers are updated
            return [u for u in self._universities if u.is_eligible(student)]

    def rank(self, student, engine) -> list[tuple[University, float]]:
        eligible = self.filter_for(student)
        scored = [(u, engine.score(student, u)) for u in eligible]
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored

    def lookup(self, uni_id: str):
        for u in self._universities:
            if u.get_uni_att('id') == uni_id:
                return u
        return None
