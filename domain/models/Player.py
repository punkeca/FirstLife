from domain.models.SkillTree import SkillTree

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hp = 100.0
        self.mana = 50.0
        self.steps = 0
        self.SkillTree = SkillTree()

    def suffer_penalty(self, hp: float, mana: float):
        self.hp = max(0, self.hp - hp)
        self.mana = max(0, self.mana - mana)

    def gain_blessing(self, hp: float, mana: float):
        self.hp += hp
        self.mana += mana

    def level_up(self):
        self.SkillTree.level_up()

    def save_state(self):
        print(f"Saving state for player {self.name}")
