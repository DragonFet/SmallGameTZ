
from game_logic import GameLogic

class Game:
    def __init__(self):
        self.game_logic = GameLogic()

    def run_start_screen(self):
        self.game_logic.draw_start_screen()

    def run_game(self):
        self.game_logic.run_game()

    def run_game_over_screen(self):
        self.game_logic.run_game_over_screen()
