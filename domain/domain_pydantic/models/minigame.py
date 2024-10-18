from typing import List
from pydantic import BaseModel, Field
from gem import Gem

class Minigame(BaseModel):
    name: str
    category: str
    gems: List[Gem] = Field(default_factory=list) 

    def start(self):
        print(f"Starting minigame: {self.name}")

    def update(self):
        print("Updating minigame...")

    def end(self):
        print(f"Ending minigame: {self.name}")

    def generate_reward(self):
        print("Generating reward for minigame.")
