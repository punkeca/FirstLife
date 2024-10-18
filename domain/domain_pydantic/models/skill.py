from pydantic import BaseModel, Field

class Skill(BaseModel):
    category: str
    description: str
    points: float = Field(default=0.0, ge=0)  # Ensure points are non-negative

    def upgrade(self):
        self.points += 10
