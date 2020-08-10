import pygame
import random, math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.jpg')
mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

player_img = pygame.image.load('ship.png')
player_x = 370
player_y = 500
player_x_change = 0

alien_img = []
alien_x = []
alien_y = []
alien_x_change = []
alien_y_change = []
aliens_n = 6

for al in range(aliens_n):
    alien_img.append(pygame.image.load('alien.png'))
    alien_x.append(random.randint(0, 730))
    alien_y.append(random.randint(50, 150))
    alien_x_change.append(1)
    alien_y_change.append(30)

bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 500
bullet_x_change = 0
bullet_y_change = 6
bullet_state = "ready"

running = True

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)

text_x = 10
text_y = 10

over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    game_over = over_font.render("Game Over! ", True, (255, 0, 0))
    screen.blit(game_over, (250, 250))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


def alien(x, y, i):
    screen.blit(alien_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def iscollision(alienx, alieny, bx, by):
    distance = math.sqrt((math.pow(alienx - bx, 2)) + (math.pow(alieny - by, 2)))
    if distance < 27:
        return True
    else:
        return False


while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change -= 2
            if event.key == pygame.K_RIGHT:
                player_x_change += 2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_x = player_x
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736

    for i in range(aliens_n):
        if alien_y[i] >440:
            for j in range(aliens_n):
                alien_y[j] = 2000
            game_over_text()
            break
        alien_x[i] += alien_x_change[i]
        if alien_x[i] <= 0:
            alien_x_change[i] = 1
            alien_y[i] += alien_y_change[i]
        elif alien_x[i] >= 736:
            alien_x_change[i] = -1
            alien_y[i] += alien_y_change[i]

        collision = iscollision(alien_x[i], alien_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bullet_y = 500
            bullet_state = "ready"
            score_value += 1
            alien_x[i] = random.randint(0, 730)
            alien_y[i] = random.randint(50, 150)

        alien(alien_x[i], alien_y[i], i)

    if bullet_y <= 0:
        bullet_y = 500
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
