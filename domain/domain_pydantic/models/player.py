from typing import List
from pydantic import BaseModel, Field
from skill_tree import SkillTree
from quest_book import QuestBook
from user import User
from goal import Goal

class Player(BaseModel):
    name: str
    hp: float = Field(default=100.0, ge=0)  # Ensure HP is non-negative
    mana: float = Field(default=50.0, ge=0)  # Ensure mana is non-negative
    steps: int = Field(default=0, ge=0)  # Ensure steps are non-negative
    skill_tree: SkillTree  
    quest_book: QuestBook 
    user: User
    goals: List[Goal] = Field(default_factory=list)

    def suffer_penalty(self, hp: float, mana: float):
        self.hp = max(0, self.hp - hp)
        self.mana = max(0, self.mana - mana)

    def gain_blessing(self, hp: float, mana: float):
        self.hp += hp
        self.mana += mana

    def level_up(self):
        self.skill_tree.level_up()

    def save_state(self):
        print(f"Saving state for player {self.name}")
