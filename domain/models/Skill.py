class Skill:
    def __init__(self, category: str, description: str, points: float):
        self.category = category
        self.description = description
        self.points = points

    def upgrade(self):
        self.points += 10
