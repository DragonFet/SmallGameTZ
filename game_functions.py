import pygame
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from startscreen import StartScreen
from gamedatabase import GameDatabase
from config import white, screen_height, screen_width, screen

def draw_start_screen():
    background_start = pygame.image.load("texture/start_background.jpg")
    scaled_background_start = pygame.transform.scale(background_start, (screen_width, screen_height))
    screen.blit(scaled_background_start, (0, 0))
    start_screen.draw()

    instructions_font = pygame.font.Font(None, 24)
    instructions_text = [
        "PageLeft - движение влево",
        "PageRight - движение вправо",
        "Space - выстрел",
        "Пропустил 5 врагов - Конец",
        "Разбился об врага - Конец"
    ]
    for i, line in enumerate(instructions_text):
        text = instructions_font.render(line, True, white)
        screen.blit(text, (10, screen_height - 100 + i * 20))

    pygame.display.flip()
    clock.tick(60)

def draw_game_over_screen():
    background_game_over = pygame.image.load("texture/game_over_background.jpg")
    scaled_background_game_over = pygame.transform.scale(background_game_over, (screen_width, screen_height))
    screen.blit(scaled_background_game_over, (0, 0))
    game_over_text = font.render("Проиграл", True, white)
    text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(game_over_text, text_rect.topleft)

    pygame.display.flip()
    pygame.time.delay(3000)

def get_player_name():
    input_prompt_font = pygame.font.Font(None, 36)
    input_prompt_text = input_prompt_font.render("Введите свой ник:", True, white)
    input_prompt_rect = input_prompt_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150))

    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 200, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                start_screen.hovered = start_screen.oval_rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_screen_active:
                    if start_screen.hovered:
                        start_screen_active = False
                else:
                    if event.button == 1:
                        if input_box.collidepoint(event.pos):
                            active = not active
                        else:
                            active = False
                        color = color_active if active else color_inactive
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        screen.fill(black)

        screen.blit(input_prompt_text, input_prompt_rect.topleft)

        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

        if not active:
            break

    return text