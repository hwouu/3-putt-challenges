# src/models/score_card.py
class ScoreCard:
    def __init__(self):
        self.scores = {}  # {course_number: shot_count}
        self.pars = {1: 3, 2: 3, 3: 3}  # 각 코스의 파 정보
        
    def add_score(self, course_number, shot_count):
        self.scores[course_number] = shot_count
        
    def get_total_score(self):
        return sum(self.scores.values())
        
    def get_total_par(self):
        return sum(self.pars.values())
        
    def get_course_result(self, course_number):
        if course_number not in self.scores:
            return None
        shot_count = self.scores[course_number]
        par = self.pars[course_number]
        return shot_count - par  # + is over par, - is under par