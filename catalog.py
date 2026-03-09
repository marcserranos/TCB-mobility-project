# Catalog.py
# Container for creating/filtering/ranking University objects

import pandas as pd
from university import University
from location import Location

class Catalog:
    def __init__(self, csv_path: str = "data/entries.csv"):
        self._csv = csv_path
        self._universities: list[University] = []

    def load(self) -> None:
        """Load CSV and convert rows into University instances."""
        try:
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
                spots=row.get('Spots available', None),
            )
            cats.append(u)

        self._universities = cats

    def all(self) -> list[University]:
        return list(self._universities)

    def rank(self, student, engine) -> list[tuple[University, float]]:
        scored = [(u, engine.score(student, u)) for u in self._universities]
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored