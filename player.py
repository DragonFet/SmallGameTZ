import pygame
from config import screen_width, screen_height
class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("texture/player.png"), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move_left(self):
        if self.rect.x > 0:
            self.rect.x -= 8

    def move_right(self):
        if self.rect.x < screen_width - self.rect.width:
            self.rect.x += 8
