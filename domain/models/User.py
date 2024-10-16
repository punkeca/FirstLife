from domain.models.Player import Player
class User:
    def __init__(self, username: str, password: str, email: str):
        self.username = username
        self.password = password
        self.email = email
        self.player

    def create_character(self, name: str):
        if(self.player): 
            return Player
        else: 
            self.player = Player(name, self)
            return self.player


    def login(self, username: str, password: str):
        return self.username == username and self.password == password

    def register(self, username: str, password: str, email: str):
        return User(username, password, email)
