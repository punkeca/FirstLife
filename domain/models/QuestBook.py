from datetime import date
from domain.models.Quest import Quest

class QuestBook:
    def __init__(self):
        self.quests = []

    def register(self, description: str, date: date):
        quest = Quest(len(self.quests) + 1, description, 100, "Adventure")
        self.quests.append(quest)

    def complete(self, quest_id: int):
        quest = next((q for q in self.quests if q.id == quest_id), None)
        if quest:
            print(f"Quest {quest.description} completed!")
        else:
            print("Quest not found.")
