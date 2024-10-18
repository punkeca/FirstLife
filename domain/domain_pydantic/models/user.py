from pydantic import BaseModel, EmailStr, Field
from player import Player 

class User(BaseModel):
    username: str
    password: str
    email: EmailStr  # Validates that the email is in the correct format
    player: Player = Field(default=None)  # Player is optional and defaults to None

    def create_character(self, name: str):
        if self.player: 
            return self.player
        else: 
            self.player = Player(name=name, user=self)
            return self.player

    def login(self, username: str, password: str):
        return self.username == username and self.password == password

    @classmethod
    def register(cls, username: str, password: str, email: str):
        return cls(username=username, password=password, email=email)
