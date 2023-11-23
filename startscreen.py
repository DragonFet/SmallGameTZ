
import pygame

from config import screen_width, screen_height,white,screen



class StartScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.start_text = self.font.render("START", True, white)
        self.start_rect = self.start_text.get_rect(center=(screen_width // 2, screen_height // 2))
        self.oval_rect = self.start_rect.inflate(20, 10)  # Увеличиваем размер овала для обводки
        self.hovered = False  # Флаг, указывающий, наведен ли курсор на START

    def draw(self):
        pygame.draw.ellipse(screen, (0, 255, 0) if self.hovered else white, self.oval_rect, 2)
        screen.blit(self.start_text, self.start_rect.topleft)