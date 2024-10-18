from datetime import date
from pydantic import BaseModel, Field

class Quest(BaseModel):
    id: int
    description: str
    date: date = Field(default_factory=date.today)  # Automatically set to today's date
    xp_points: float
    category: str

    def distribute_xp(self) -> float:
        return self.xp_points
