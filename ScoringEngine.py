import math
# This class is for scoring and ranking universities based on student profiles.

class ScoringEngine:
    def __init__(self, weights: dict = None):
        """Initialize the scoring engine with optional weights."""
        self._weights = weights or {}

    def score(self, student_obj, university_obj) -> float:
        """Compute affinity score based on student preferences."""
        prefs = student_obj.get_preferences()
        if not prefs:
            return 0.0

        # check eligibility, if not eligible, score is 0
        if not self.is_eligible(student_obj, university_obj):
            return 0.0

        # weights reflect inverse of position importance: 1st pref has weight 4
        weights = [4, 3, 2, 1]
        total = 0.0

        for i, pref in enumerate(prefs):
            if i >= 4:  # only 4 preferences supported
                break
            weight = weights[i]
            val = self._preference_value(pref, university_obj)
            total += weight * val

        return total # returns the affinity scrore

    def _preference_value(self, pref, university_obj) -> float:
        """Return a 0-10 numeric value for a preference from the university."""

        try:
            if pref == 'Cost of Living':
                val = university_obj.get_uni_att('cost_of_living')
                return float(val) if val is not None and str(val) != '' else 0.0
            elif pref == 'Nightlife':
                val = university_obj.get_uni_att('nightlife')
                return float(val) if val is not None and str(val) != '' else 0.0
            elif pref == 'Academic Rank':
                # university stores a ranking which might be numeric or a range
                raw = university_obj.get_uni_att('ranking')
                if raw is None or str(raw) == '':
                    return 0.0
                # try to extract a numeric rank (take first number if range like "451-500")
                try:
                    s = str(raw)
                    # extract first contiguous digits
                    import re
                    m = re.search(r"(\d+)", s)
                    if m:
                        rank_val = int(m.group(1))
                        return self.calculate_academic_score(rank_val)
                except Exception:
                    return 0.0
                return 0.0
            elif pref == 'Weather':
                # weather is now numeric 1-10
                val = university_obj.get_uni_att('weather')
                try:
                    return float(val) if val is not None and str(val) != '' else 0.0
                except Exception:
                    return 0.0
        except Exception:
            pass
        return 0.0

    @staticmethod
    def calculate_academic_score(rank, max_rank=1500, decay_factor=5.5):
        """Transform a raw academic rank into a 0-10 score. 
        Uses the specified power-log formula to create a plateau at the top."""

        try:
            rank = float(rank)
        except Exception:
            return 0.0

        if rank <= 1:
            return 10.0
        if rank >= max_rank:
            return 0.0

        log_rank = math.log10(rank)
        log_max = math.log10(max_rank)
        score = 10 * (1 - (log_rank / log_max) ** decay_factor)
        return round(score, 1)

    def rank(self, student_obj, universities: list) -> list[tuple]:
        """Score and sort a list of universities and scores for a given student.
        Ineligible universities will have a score of 0.
        """
        scored = []
        for uni in universities:
            score = self.score(student_obj, uni)
            scored.append((uni, score))
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored

    def is_eligible(self, student_obj, university_obj) -> bool:
        """Check if the student meets the university's eligibility criteria."""

        # minimum grade check
        stud_grade = student_obj.get_grade()
        uni_min_grade = university_obj.get_uni_att('grade')
        try:
            uni_min_grade = float(uni_min_grade) if uni_min_grade is not None else 0.0
        except Exception:
            uni_min_grade = 0.0
        if stud_grade < uni_min_grade:
            return False

        # degree matching
        stud_deg = student_obj.get_degree()
        uni_degs = university_obj.get_uni_att('degree')
        if stud_deg and uni_degs:
            if stud_deg not in uni_degs:
                return False

        # continent requirement
        cont = None
        loc = university_obj.get_uni_att('location')
        if isinstance(loc, dict):
            cont = loc.get('continent')
        elif hasattr(loc, 'get_continent'):
            cont = loc.get_continent()
        if cont and student_obj.get_continents():
            if cont not in student_obj.get_continents():
                return False

        # language requirements
        req_langs = {}
        if hasattr(university_obj, '_University__lang_levels'):
            req_langs = university_obj._University__lang_levels or {}
        if not req_langs:
            langs = university_obj.get_uni_att('lang')
            if isinstance(langs, list):
                for l in langs:
                    req_langs[l] = ''
            elif isinstance(langs, str):
                for l in langs.split(';'):
                    l = l.strip()
                    if l:
                        req_langs[l] = ''

        if req_langs:
            stud_langs = student_obj.get_languages() or {}
            order = {'B1': 1, 'B2': 2, 'C1': 3, 'C2': 4}
            passed = False
            for ul, required_level in req_langs.items():
                if ul in stud_langs and stud_langs[ul]:
                    if required_level:
                        s_val = order.get(stud_langs[ul], 0)
                        u_val = order.get(required_level, 0)
                        if s_val >= u_val:
                            passed = True
                            break
                    else:
                        passed = True
                        break
            if not passed:
                return False
        return True