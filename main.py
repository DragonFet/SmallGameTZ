import  sys
import pygame
from game_logic import GameLogic
from game import Game

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
white = (255, 255, 255)

game = Game()
game_logic = GameLogic()

# Основной цикл стартового экрана
while game_logic.start_screen_active:
    game_logic.draw_start_screen()

# Основной цикл игры
while game_logic.running:
    game_logic.run_game()

# Экран "Проиграл"
game_logic.run_game_over_screen()

pygame.quit()
sys.exit()
