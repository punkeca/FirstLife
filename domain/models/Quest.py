from datetime import date

class Quest:
    def __init__(self, quest_id: int, description: str, xp_points: float, category: str):
        self.id = quest_id
        self.description = description
        self.date = date.today()
        self.xp_points = xp_points
        self.category = category

    def distribute_xp(self):
        return self.xp_points
