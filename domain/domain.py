from datetime import date
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel
from sqlmodel import Session
from datetime import date



from typing import Optional, List

from sqlmodel import create_engine


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=40, index=True, unique=True)
    password: str = Field(max_length=40, index=True)
    email: str = Field(max_length=100, index=True, unique=True)
    player: Optional['Player'] = Relationship(back_populates="user", sa_relationship_kwargs={"uselist": False})  
'''
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

'''

class Player(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=40, index=True)
    hp: float = Field(default=100.0, ge=0)
    mana: float = Field(default=50.0, ge=0)
    steps: int = Field(default=0, ge=0)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional['User'] = Relationship(back_populates="player")
    goals: List['Goal'] = Relationship(back_populates="player")

      # One-to-one relationship: Player -> SkillTree
    skill_tree: Optional["SkillTree"] = Relationship(
        back_populates="player", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # One-to-one relationship: Player -> QuestBook
    quest_book: Optional["QuestBook"] = Relationship(
        back_populates="player", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class SkillTree(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    level: int = Field(default=1, ge=1)  # Ensure level is at least 1
    xp: float = Field(default=0.0, ge=0)  # Ensure XP is non-negative
    specialty: Optional[str] = Field(max_length=40, default=None)
    player_id: Optional[int] = Field(default=None, foreign_key="player.id")  # Link to Player

    # One-to-Many relationship: SkillTree -> Skills
    skills: List["Skill"] = Relationship(
        back_populates="skill_tree",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # Relationship with Player
    player: Optional["Player"] = Relationship(back_populates="skill_tree")

    def level_up(self):
        self.level += 1
        self.xp = 0

    def update_player(self):
        print("Updating player based on skill tree.")

class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    category: str = Field(max_length=40)
    description: str = Field(max_length=200)
    points: float = Field(default=0.0, ge=0)  # Ensure points are non-negative

    # Foreign key linking Skill to SkillTree
    skill_tree_id: Optional[int] = Field(default=None, foreign_key="skilltree.id")

    # Back-populate the relationship with SkillTree
    skill_tree: Optional["SkillTree"] = Relationship(back_populates="skills")

    def upgrade(self):
        self.points += 10


class QuestBook(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)

     # Foreign key linking QuestBook to Player
    player_id: Optional[int] = Field(default=None, foreign_key="player.id")

    # Back-populate the relationship with Player
    player: Optional["Player"] = Relationship(back_populates="quest_book")

    # One-to-Many relationship: QuestBook -> Quests
    quests: List["Quest"] = Relationship(
        back_populates="quest_book", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def register(self, description: str):
        # Create a new quest and add it to the quest book
        quest_id = len(self.quests) + 1
        quest = Quest(
            id=quest_id,
            description=description,
            category="Adventure",
            xp_points=50.0,  # Default xp_points
            quest_book_id=self.id  # Link the quest to this quest book
        )
        self.quests.append(quest)

    def complete(self, quest_id: int):
        # Find and complete the quest with the given ID
        quest = next((q for q in self.quests if q.id == quest_id), None)
        if quest:
            print(f"Quest '{quest.description}' completed!")
        else:
            print("Quest not found.")


class Quest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str = Field(max_length=200)
    qdate: date = Field(default_factory=date.today)  # Set date to today's date
    xp_points: float = Field(default=0.0, ge=0)  # Non-negative XP points
    category: str = Field(max_length=40)

    # Foreign key linking Quest to Goal
    goal_id: Optional[int] = Field(default=None, foreign_key="goal.id")

    # Back-populate relationship with Goal
    goal: Optional["Goal"] = Relationship(back_populates="quests")

    # Foreign key linking Quest to QuestBook
    quest_book_id: Optional[int] = Field(default=None, foreign_key="questbook.id")

    # Back-populate relationship with QuestBook
    quest_book: Optional["QuestBook"] = Relationship(back_populates="quests")

    def distribute_xp(self) -> float:
        return self.xp_points


class Goal(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    description: str = Field(max_length=200)
    category: str = Field(max_length=40)
    reward: str = Field(max_length=40)
    progress: int = Field(default=0, ge=0, le=100)  

    player_id: Optional[int] = Field(default=None, foreign_key="player.id")
    player: Optional["Player"] = Relationship(back_populates="goals")
    quests: List['Quest'] = Relationship(back_populates="goal", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

    def update(self, progress: int):
        self.progress = min(100, self.progress + progress)

    def generate_quests(self, ai_service) -> ['Quest']:
        quests = ai_service.generate_quests(self.description)
        self.quests.extend(quests)
        return quests
    
  

usuario_bd='firstlife'
senha_bd='firstlife'
host_bd='localhost'
banco_bd='firstlife'
url_bd = f"mariadb+pymysql://{usuario_bd}:{senha_bd}@{host_bd}:3306/{banco_bd}?charset=utf8mb4"
engine = create_engine(url_bd, echo=True)  

if __name__=="__main__":    
    SQLModel.metadata.create_all(engine) 
    with Session(engine) as se:
         # Create a user
        user = User(id=1, username="admin", password="admin", email="admin@example.com")

        # Create a player associated with the user
        player = Player(id=1, name="Hero", user=user)

        # Create a skill tree for the player
        skill_tree = SkillTree(id=1, level=1, xp=0.0, specialty="Magic", player=player)

        # Add skills to the skill tree
        fire_skill = Skill(id=1, category="Fire", description="Casts fireballs", points=10.0, skill_tree=skill_tree)
        water_skill = Skill(id=2, category="Water", description="Controls water", points=15.0, skill_tree=skill_tree)

        # Create a quest book for the player
        quest_book = QuestBook(id=1, player=player)

        # Add quests to the quest book
        quest1 = Quest(id=1, description="Find the Sword", category="Adventure", xp_points=50.0, quest_book=quest_book)
        quest2 = Quest(id=2, description="Defeat the Dragon", category="Combat", xp_points=100.0, quest_book=quest_book)

        # Create a goal for the player
        goal = Goal(id=1, description="Become a Hero", category="Achievement", reward="Hero Badge", progress=50, player=player)

        # Link quests to the goal
        goal.quests.extend([quest1, quest2])

        # Add all objects to the session and commit
        se.add_all([user, player, skill_tree, fire_skill, water_skill, quest_book, quest1, quest2, goal])
        se.commit()