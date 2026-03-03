import math

# This class is responsible for scoring and ranking universities based on student profiles.
class ScoringEngine:
    def __init__(self, weights: dict = None):
        # weight dictionary may map preference names to explicit weights; if
        # None, we simply weight by position in the preference list.
        self._weights = weights or {}

    def affinity_score(self, student_obj, university_obj) -> float:
        """Compute affinity score based on student preferences.

        Each preference value from the university (0-10 range) is multiplied by
        a weight based on the preference position:
        - Position 1 (1st preference): weight = 4
        - Position 2 (2nd preference): weight = 3
        - Position 3 (3rd preference): weight = 2
        - Position 4 (4th preference): weight = 1

        Max score is 100 (when all uni attributes are 10 and all weights sum to 10).
        Min score is 0.
        """
        prefs = student_obj.get_preferences()
        if not prefs:
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

        return total

    def _preference_value(self, pref, university_obj) -> float:
        """Return a 0-10 numeric value for a preference from the university.

        Maps preference names to university attributes.
        """
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

        Uses the specified power-log formula to create a plateau at the top.
        """
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

    def risk_score(self, student_obj, university_obj) -> float:
        """Penalty related to how far the student is above the cutoff."""
        grade = student_obj.get_grade()
        cutoff = university_obj.get_uni_att('cutoff_grade')
        try:
            cutoff = float(cutoff)
        except Exception:
            cutoff = 0.0

        if grade < cutoff:
            return cutoff - grade
        else:
            return 0.0

    def rank(self, student_obj, universities: list) -> list[tuple]:
        """Score and sort a list of universities for a given student.

        The returned value is a list of ``(university, score)`` tuples sorted in
        descending order of score.  Basic eligibility is checked via
        :meth:`is_eligible` so callers can provide a full catalog or the result
        of :meth:`Catalog.filter_for` as they wish.
        """
        scored = []
        for uni in universities:
            if not self.is_eligible(student_obj, uni):
                continue
            score = self.affinity_score(student_obj, uni)
            scored.append((uni, score))
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored

    def is_eligible(self, student_obj, university_obj) -> bool:
        """Return **True** when the student satisfies basic university requirements.

        The method compares information from both objects rather than relying on
        a single class:

        * **minimum_grade** - the student's grade must be equal or greater than
          the university's minimum grade requirement.
        * **degree** - the student's degree string must appear in the
          university's list of accepted degrees (if either side has data).
        * **continents** - the university's continent (from its location) should
          match at least one of the continents listed in the student's profile.
        * **languages** - the university may specify required languages, each
          optionally paired with a minimum level (B1, B2, C1, C2).  The student
          must have *at least one* of those languages and their certification
          level must be equal or higher than the required level.  The level
          ordering is: ``B1 < B2 < C1 < C2``.  If the university only lists
          languages without levels, any presence of that language in the
          student's profile is sufficient.
        """

        # minimum grade check
        stud_grade = student_obj.get_grade()
        uni_min_grade = university_obj.get_uni_att('grade')
        try:
            uni_min_grade = float(uni_min_grade) if uni_min_grade is not None else 0.0
        except Exception:
            uni_min_grade = 0.0
        if stud_grade < uni_min_grade:
            return False

        # ara per ara ho eliminem fins que no sabem que fer amb el degree
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

        # language requirements, possibly with levels
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