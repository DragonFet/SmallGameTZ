import pygame

from config import screen_width, screen_height
import random


class Enemy:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("texture/enemy.png"), (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move_down(self, speed):
        self.rect.y += speed
        if self.rect.y > screen_height:
            self.reset_position()

    def reset_position(self):
        self.rect.y = 50
        self.rect.x = random.randint(0, screen_width - random.randint(10, 50))
