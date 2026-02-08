# scoring.py

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
    