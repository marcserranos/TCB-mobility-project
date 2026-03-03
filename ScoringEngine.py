# This class is responsible for scoring and ranking universities based on student profiles.
class ScoringEngine:
    def __init__(self, weights: dict = None):
        # weight dictionary may map preference names to explicit weights; if
        # None, we simply weight by position in the preference list.
        self._weights = weights or {}

    def affinity_score(self, student_obj, university_obj) -> float:
        """Compute a score based on the student's ordered preferences.

        The first preference has the greatest influence, the second less, etc.
        Values are normalised to the interval [0,1] for comparability.
        """
        prefs = student_obj.get_preferences()
        if not prefs:
            return 0.0

        n = len(prefs)
        weights = []
        if self._weights:
            for p in prefs:
                weights.append(self._weights.get(p, 1.0))
            total_weight = sum(weights)
        else:
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)

        total = 0.0
        for w, pref in zip(weights, prefs):
            val = self._preference_value(pref, university_obj)
            total += w * val

        if total_weight <= 0:
            return 0.0
        return total / (total_weight * 10)

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

    def rank(self) -> tuple:
        """Returns a list of tuples with both the risk_score and the overall ranking of each university"""
        return ()