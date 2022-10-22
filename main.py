# Space Invader using pygame
# entity images from flaticon.com
# background from freepik.com
# CTRL + ALT + L = format

import pygame
from pygame import mixer
import random
import math

# Initialize the pygame
pygame.init()

# create the screen (height: 800, width: 600
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')
mixer.music.load('background.wav')
# mixer.music so it plays continuously
mixer.music.play(-1)  # -1 plays in the loop

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370  # can't be exactly half...need to consider image size
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# Bullet
# Ready - you can't see bullet on screen
# Fire - bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = playerX  # can't be exactly half...need to consider image size
bulletY = 480
bulletX_change = 0
bulletY_change = 0.7
bulletState = "ready"

# Score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 45)
textX = 10
textY = 10

# Game Over Text
game_over_font = pygame.font.Font('freesansbold.ttf', 80)
final_score_font = pygame.font.Font('freesansbold.ttf', 80)


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (160, 200))
    score = final_score_font.render("FINAL SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (115, 300))


def player(x, y):
    screen.blit(playerImg, (x, y))  # without parentheses, x and y not bot included in dest param


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def collision_check(enemyXValue, enemyYValue, bulletXValue, bulletYValue):
    distance = math.sqrt((math.pow(enemyXValue - bulletXValue, 2)) + (math.pow(enemyYValue - bulletYValue, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB - Red, Green, Blue
    # to find colors look up "color to rgb"
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # all caps for syntax
            running = False

        # if key is pressed, check whether it's right/left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:  # can only fire one at a time
                if bulletState == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking for boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # 800 - 64 pixels
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # 800 - 64 pixels
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = collision_check(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            # TODO: make function
            bulletY = 480
            bulletState = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"
    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()