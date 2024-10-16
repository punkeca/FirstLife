class Gem:
    def __init__(self, description: str, category: str, power: float):
        self.description = description
        self.category = category
        self.power = power

    def level_up(self):
        self.power *= 1.1
