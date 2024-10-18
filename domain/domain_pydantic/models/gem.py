from pydantic import BaseModel, Field

class Gem(BaseModel):
    description: str
    category: str
    power: float = Field(default=100.0)

    def __init__(self, **data):
        super().__init__(**data) #pydantic deals with initialization
        
        if self.power < 0:
            raise ValueError("Power must be a non-negative value")

    def level_up(self):
        self.power *= 1.1