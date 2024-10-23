from datetime import date
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel
from sqlmodel import Session

from typing import Optional, List

from sqlmodel import create_engine


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=40, index=True, unique=True)
    password: str = Field(max_length=40, index=True)
    email: str = Field(index=True, unique=True)
    player_id: Optional[int] = Field(default=None, foreign_key="player.id")
    player: Optional['Player'] = Relationship(back_populates="users")  

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



class Player(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    hp: float = Field(default=100.0, ge=0)
    mana: float = Field(default=50.0, ge=0)
    steps: int = Field(default=0, ge=0)
    skill_tree_id: Optional[int] = Field(default=None, foreign_key="skilltree.id")
    quest_book_id: Optional[int] = Field(default=None, foreign_key="questbook.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    goals: List['Goal'] = Relationship(back_populates="player")

    skill_tree: Optional['SkillTree'] = Relationship()
    quest_book: Optional['QuestBook'] = Relationship()
    user: Optional[User] = Relationship()

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
    



class SkillTree(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    level: int = Field(default=1, ge=1)  # Ensure level is at least 1
    xp: float = Field(default=0.0, ge=0)  # Ensure XP is non-negative
    specialty: Optional[str] = None  # Specialty can be optional
    player_id: Optional[int] = Field(default=None, foreign_key="player.id")  # Link to Player
    skills: List['Skill'] = Relationship(back_populates="skill_tree", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    gems: List['Gem'] = Relationship(back_populates="skill_tree", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    
    player: Optional[Player] = Relationship()

    def level_up(self):
        self.level += 1
        self.xp = 0

    def update_player(self):
        print("Updating player based on skill tree.")



class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    category: str
    description: str
    points: float = Field(default=0.0, ge=0)  # Ensure points are non-negative

    def upgrade(self):
        self.points += 10

class QuestBook(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    quests: List['Quest'] = Relationship(back_populates="quest_book", sa_relationship_kwargs={"cascade": "all, delete-orphan"})  # Initialize with an empty list

    def register(self, description: str):
        quest_id = len(self.quests) + 1
        quest = Quest(id=quest_id, description=description, reward=100, category="Adventure", xp_points=50.0)  # Set default xp_points
        self.quests.append(quest)

    def complete(self, quest_id: int):
        quest = next((q for q in self.quests if q.id == quest_id), None)
        if quest:
            print(f"Quest '{quest.description}' completed!")
        else:
            print("Quest not found.")

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


class Quest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str
    date: date = Field(default_factory=date.today)  # Automatically set to today's date
    xp_points: float
    category: str
    quest_book_id: Optional[int] = Field(default=None, foreign_key="questbook.id")

    def distribute_xp(self) -> float:
        return self.xp_points
    




class Goal(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str
    category: str
    reward: str
    progress: int = Field(default=0, ge=0, le=100)  # Ensures progress is between 0 and 100
    quests: List[Quest] = Relationship(back_populates="goal", sa_relationship_kwargs={"cascade": "all, delete-orphan"})  # Proper relationship


    def update(self, progress: int):
        self.progress = min(100, self.progress + progress)

    def generate_quests(self, ai_service) -> ['Quest']:
        quests = ai_service.generate_quests(self.description)
        self.quests.extend(quests)
        return quests
    

class Gem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str
    category: str
    power: float = Field(default=100.0)

    def __init__(self, **data):
        super().__init__(**data) #pydantic deals with initialization
        
        if self.power < 0:
            raise ValueError("Power must be a non-negative value")

    def level_up(self):
        self.power *= 1.1

    
usuario_bd='firstlife'
senha_bd='firstlife'
host_bd='localhost'
banco_bd='firstlife'
url_bd = f"mariadb+pymysql://{usuario_bd}:{senha_bd}@{host_bd}:3306/{banco_bd}?charset=utf8mb4"
engine = create_engine(url_bd, echo=True)  

if __name__=="__main__":    
    SQLModel.metadata.create_all(engine) 
    with Session(engine) as se: 
        #create an instance of your class
        #se.add(<yourclassvar>)
        se.commit()