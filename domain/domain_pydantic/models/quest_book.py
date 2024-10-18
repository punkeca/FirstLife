from datetime import date
from typing import List
from pydantic import BaseModel, Field
from quest import Quest 

class QuestBook(BaseModel):
    quests: List[Quest] = Field(default_factory=list)  # Initialize with an empty list

    def register(self, description: str, quest_date: date):
        quest_id = len(self.quests) + 1
        quest = Quest(id=quest_id, description=description, reward=100, category="Adventure")
        self.quests.append(quest)

    def complete(self, quest_id: int):
        quest = next((q for q in self.quests if q.id == quest_id), None)
        if quest:
            print(f"Quest '{quest.description}' completed!")
        else:
            print("Quest not found.")
