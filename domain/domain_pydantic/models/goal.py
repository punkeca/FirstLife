from typing import List
from pydantic import BaseModel, Field
from quest import Quest 

class Goal(BaseModel):
    description: str
    category: str
    reward: str
    progress: int = Field(default=0, ge=0, le=100)  # Ensures progress is between 0 and 100
    quests: List[Quest] = []

    def update(self, progress: int):
        self.progress = min(100, self.progress + progress)

    def generate_quests(self, ai_service) -> List[Quest]:
        quests = ai_service.generate_quests(self.description)
        self.quests.extend(quests)
        return quests
