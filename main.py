import pygame
import random
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from startscreen import StartScreen
from gamedatabase import GameDatabase

pygame.init()
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space War 2")

background = pygame.image.load("texture/background.png")

if background.get_rect().size != (screen_width, screen_height):
    print("Error: Background image size does not match the screen size.")
    pygame.quit()
    sys.exit()

player = Player(screen_width // 2 - 25, screen_height - 50)
enemies = [Enemy(random.randint(0, screen_width - 50), 50) for _ in range(2)]
bullets = []

pygame.mixer.init()
pygame.mixer.music.load("music/background_music.mp3")
shoot_sound = pygame.mixer.Sound("music/shoot_sound.mp3")
pygame.mixer.music.play(-1)

start_screen = StartScreen()

# Инициализация базы данных
db = GameDatabase()

# Основной цикл
start_screen_active = True
while start_screen_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            start_screen.hovered = start_screen.oval_rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if start_screen.hovered:
                start_screen_active = False

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

# Основной цикл игры
running = True
clock = pygame.time.Clock()
missed_enemies = 0
score = 0  # Добавлен счетчик очков
player_collided_with_enemy = False  # Добавлен флаг для столкновения игрока с врагом

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_RIGHT]:
        player.move_right()

    if pygame.time.get_ticks() % 65 == 0:
        new_enemy = Enemy(random.randint(0, screen_width - 50), 50)
        enemies.append(new_enemy)

    if keys[pygame.K_SPACE]:
        bullet = Bullet(player.rect.x + player.rect.width // 2 - 2, player.rect.y)
        bullets.append(bullet)
        shoot_sound.play()

    bg_width, bg_height = background.get_rect().size
    scale_factor_x = screen_width / bg_width
    scale_factor_y = screen_height / bg_height
    scaled_background = pygame.transform.scale(background, (screen_width, screen_height))

    screen.blit(scaled_background, (0, 0))

    for bullet in bullets[:]:
        bullet.move_up(5)
        screen.blit(bullet.image, bullet.rect.topleft)
        for enemy in enemies[:]:
            if bullet.rect.colliderect(enemy.rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                # Увеличение счета при исчезновении врага
                score += 2

    font = pygame.font.Font(None, 36)
    score_display = font.render(f"Score: {score}", True, white)
    screen.blit(score_display, (10, 10))

    screen.blit(player.image, player.rect.topleft)

    for enemy in enemies:
        enemy.move_down(2)
        screen.blit(enemy.image, enemy.rect.topleft)

        if player.rect.colliderect(enemy.rect):
            print("Game Over: Your ship collided with an enemy!")
            player_collided_with_enemy = True
            running = False

        if enemy.rect.y > screen_height:
            missed_enemies += 1
            enemies.remove(enemy)

    if missed_enemies >= 5:
        print("Game Over: You missed too many enemies!")
        running = False

    pygame.display.flip()

    clock.tick(60)

# Экран "Проиграл"
background_game_over = pygame.image.load("texture/game_over_background.jpg")
scaled_background_game_over = pygame.transform.scale(background_game_over, (screen_width, screen_height))
screen.blit(scaled_background_game_over, (0, 0))
game_over_text = font.render("Проиграл", True, white)
text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
screen.blit(game_over_text, text_rect.topleft)

pygame.display.flip()
pygame.time.delay(3000)

if not running:  # Добавлено условие для вывода таблицы и ввода имени
    # Ввод имени игрока
    input_prompt_font = pygame.font.Font(None, 36)
    input_prompt_text = input_prompt_font.render("Введите свой ник:", True, white)
    input_prompt_rect = input_prompt_text.get_rect(center=(screen_width // 2, screen_height // 2 + 150))

    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 200, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
    text = ''

    # Основной цикл ввода имени
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
                    if event.button == 1:  # Левая кнопка
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

    # Вставка текущего счета и имени игрока в базу данных
    db.insert_score(text, score)

    if not start_screen_active:
        # Отображение таблицы лидеров
        background_leaderboard = pygame.image.load("texture/leaderboard_background.jpg")
        scaled_background_leaderboard = pygame.transform.scale(background_leaderboard, (screen_width, screen_height))
        screen.blit(scaled_background_leaderboard, (0, 0))
        leaderboard_text = font.render("Таблица лидеров", True, white)
        screen.blit(leaderboard_text, (screen_width // 2 - 150, 20))

        top_scores = db.get_top_scores()
        for i, row in enumerate(top_scores):
            entry_text = f"{i + 1}. {row[1]}: {row[2]}"
            entry_render = font.render(entry_text, True, white)
            screen.blit(entry_render, (screen_width // 2 - 100, 80 + i * 40))

        pygame.display.flip()
        pygame.time.delay(10000)

    clock.tick(60)

pygame.quit()
sys.exit()