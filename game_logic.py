
import pygame
import random
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from startscreen import StartScreen
from gamedatabase import GameDatabase
from config import white, screen_height, screen_width, screen

class GameLogic:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.black = (0, 0, 0)
        self.background = pygame.image.load("texture/background.png")
        self.font = pygame.font.Font(None, 36)
        self.player = Player(screen_width // 2 - 25, screen_height - 50)
        self.enemies = [Enemy(random.randint(0, screen_width - 50), 50) for _ in range(2)]
        self.bullets = []

        pygame.mixer.init()
        pygame.mixer.music.load("music/background_music.mp3")
        self.shoot_sound = pygame.mixer.Sound("music/shoot_sound.mp3")
        pygame.mixer.music.play(-1)

        self.start_screen = StartScreen()
        self.db = GameDatabase()

        self.start_screen_active = True
        self.running = True
        self.missed_enemies = 0
        self.score = 0
        self.player_collided_with_enemy = False

    def draw_start_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                self.start_screen.hovered = self.start_screen.oval_rect.collidepoint(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_screen.hovered:
                    self.start_screen_active = False

        background_start = pygame.image.load("texture/start_background.jpg")
        scaled_background_start = pygame.transform.scale(background_start, (screen_width, screen_height))
        screen.blit(scaled_background_start, (0, 0))
        self.start_screen.draw()

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
        self.clock.tick(60)

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        if keys[pygame.K_RIGHT]:
            self.player.move_right()

        if pygame.time.get_ticks() % 65 == 0:
            new_enemy = Enemy(random.randint(0, screen_width - 50), 50)
            self.enemies.append(new_enemy)

        if keys[pygame.K_SPACE]:
            bullet = Bullet(self.player.rect.x + self.player.rect.width // 2 - 2, self.player.rect.y)
            self.bullets.append(bullet)
            self.shoot_sound.play()

        bg_width, bg_height = self.background.get_rect().size
        scale_factor_x = screen_width / bg_width
        scale_factor_y = screen_height / bg_height
        scaled_background = pygame.transform.scale(self.background, (screen_width, screen_height))

        screen.blit(scaled_background, (0, 0))

        for bullet in self.bullets[:]:
            bullet.move_up(5)
            screen.blit(bullet.image, bullet.rect.topleft)
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 2

        score_display = self.font.render(f"Score: {self.score}", True, white)
        screen.blit(score_display, (10, 10))

        screen.blit(self.player.image, self.player.rect.topleft)

        for enemy in self.enemies:
            enemy.move_down(2)
            screen.blit(enemy.image, enemy.rect.topleft)

            if self.player.rect.colliderect(enemy.rect):
                print("Game Over: Your ship collided with an enemy!")
                self.player_collided_with_enemy = True
                self.running = False

            if enemy.rect.y > screen_height:
                self.missed_enemies += 1
                self.enemies.remove(enemy)

        if self.missed_enemies >= 5:
            print("Game Over: You missed too many enemies!")
            self.running = False

        pygame.display.flip()
        self.clock.tick(60)

    def run_game_over_screen(self):
        self.draw_game_over_screen()

        if not self.running:
            player_name = self.get_player_name()

            self.db.insert_score(player_name, self.score)

            background_leaderboard = pygame.image.load("texture/leaderboard_background.jpg")
            scaled_background_leaderboard = pygame.transform.scale(background_leaderboard, (screen_width, screen_height))
            screen.blit(scaled_background_leaderboard, (0, 0))
            leaderboard_text = self.font.render("Таблица лидеров", True, white)
            screen.blit(leaderboard_text, (screen_width // 2 - 150, 20))

            top_scores = self.db.get_top_scores()
            for i, row in enumerate(top_scores):
                entry_text = f"{i + 1}. {row[1]}: {row[2]}"
                entry_render = self.font.render(entry_text, True, white)
                screen.blit(entry_render, (screen_width // 2 - 100, 80 + i * 40))

            pygame.display.flip()
            pygame.time.delay(10000)

    def draw_game_over_screen(self):
        background_game_over = pygame.image.load("texture/game_over_background.jpg")
        scaled_background_game_over = pygame.transform.scale(background_game_over, (screen_width, screen_height))
        screen.blit(scaled_background_game_over, (0, 0))
        game_over_text = self.font.render("Проиграл", True, white)
        text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, text_rect.topleft)

        pygame.display.flip()
        pygame.time.delay(3000)

    def get_player_name(self):
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
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
            screen.fill(self.black)
            screen.blit(input_prompt_text, input_prompt_rect.topleft)

            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)

            pygame.display.flip()
            self.clock.tick(30)

            if not active:
                break

        return text
