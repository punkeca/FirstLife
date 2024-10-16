from typing import List
from domain.models.Quest import Quest

class Goal:
    def __init__(self, description: str, category: str, reward: str):
        self.description = description
        self.category = category
        self.reward = reward
        self.progress = 0
        self.quests: List[Quest] = []

    def update(self, progress: int):
        self.progress = min(100, self.progress + progress)

    def generate_quests(self, ai_service) -> List[Quest]:
        quests = ai_service.generate_quests(self.description)
        self.quests.extend(quests)
        return quests
