class SkillTree:
    def __init__(self):
        self.level = 1
        self.xp = 0.0
        self.specialty = None

    def level_up(self):
        self.level += 1
        self.xp = 0

    def update_player(self):
        print("Updating player based on skill tree.")

    #def restart_leveling_system(self):
        self.xp = 0
