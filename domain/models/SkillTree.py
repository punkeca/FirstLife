from domain.models.Player import Player

class SkillTree:
    def __init__(self, player: Player):
        self.level = 1
        self.xp = 0.0
        self.specialty = None
        self.player = None
        self.skills = []
        self.gem = []

    def level_up(self):
        self.level += 1
        self.xp = 0

    def update_player(self):
        print("Updating player based on skill tree.")

    #def restart_leveling_system(self):
        #self.xp = 0
