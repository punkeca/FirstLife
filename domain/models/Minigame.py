class Minigame:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category

    def start(self):
        print(f"Starting minigame: {self.name}")

    def update(self):
        print("Updating minigame...")

    def end(self):
        print(f"Ending minigame: {self.name}")

    def generate_reward(self):
        print("Generating reward for minigame.")
