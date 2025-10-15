import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Clock for FPS
clock = pygame.time.Clock()

# Load and scale images
playerImg = pygame.transform.scale(pygame.image.load("player.png"), (64, 64))
bulletImg = pygame.transform.scale(pygame.image.load("bullet.png"), (8, 24))
enemyImg = pygame.transform.scale(pygame.image.load("alien.png"), (48, 48))

# Player setup
playerX = WIDTH // 2 - 32
playerY = HEIGHT - 80
playerX_change = 0

# Bullet setup
bulletX = 0
bulletY = playerY
bulletY_change = 10
bullet_state = "ready"

# Enemy setup
num_of_enemies = 6
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, WIDTH - 48))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(40)

# Score and lives
score_value = 0
lives = 3
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 64)

def show_score():
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (10, 10))

def show_lives():
    life_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(life_text, (WIDTH - 120, 10))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 28, y))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    return distance < 27

def show_game_over():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 32))

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))  # Black background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    # Player movement
    playerX += playerX_change
    playerX = max(0, min(playerX, WIDTH - 64))

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"

    # Enemy movement
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0 or enemyX[i] >= WIDTH - 48:
            enemyX_change[i] *= -1
            enemyY[i] += enemyY_change[i]

        # Collision
        if is_collision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = playerY
            bullet_state = "ready"
            score_value += 10
            enemyX[i] = random.randint(0, WIDTH - 48)
            enemyY[i] = random.randint(50, 150)

        # Game over condition
        if enemyY[i] > HEIGHT - 120:
            lives = 0

        enemy(enemyX[i], enemyY[i])

    # Game over
    if lives <= 0:
        show_game_over()
    else:
        player(playerX, playerY)

    show_score()
    show_lives()
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
