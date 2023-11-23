import pygame

class Bullet:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load("texture/bullet.png"), (4, 10))
        self.rect = self.image.get_rect(topleft=(x, y))

    def move_up(self, speed):
        self.rect.y -= speed