from typing import List, Optional
from pydantic import BaseModel, Field
from player import Player 
from skill import Skill
from gem import Gem

class SkillTree(BaseModel):
    level: int = Field(default=1, ge=1)  # Ensure level is at least 1
    xp: float = Field(default=0.0, ge=0)  # Ensure XP is non-negative
    specialty: Optional[str] = None  # Specialty can be optional
    player: Optional[Player] = None  # Player can be set later
    skills: List[Skill] = Field(default_factory=list)  
    gems: List[Gem] = Field(default_factory=list) 

    def level_up(self):
        self.level += 1
        self.xp = 0

    def update_player(self):
        print("Updating player based on skill tree.")

    # Uncomment if you want to restart the leveling system
    # def restart_leveling_system(self):
    #     self.xp = 0
