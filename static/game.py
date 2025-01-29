import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Killer Bean - PC Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game clock
clock = pygame.time.Clock()

# Player settings
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10
player_speed = 5

# Bullet settings
bullet_width, bullet_height = 10, 20
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width, enemy_height = 50, 50
enemy_speed = 3
enemies = []

# Font settings
font = pygame.font.SysFont(None, 30)

# Game Over flag
game_over = False

# Draw player
def draw_player(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, player_width, player_height))

# Draw bullet
def draw_bullet(bullet):
    pygame.draw.rect(screen, RED, bullet)

# Draw enemy
def draw_enemy(enemy):
    pygame.draw.rect(screen, GREEN, enemy)

# Main game loop
def game_loop():
    global player_x, player_y, bullets, enemies, game_over

    # Game loop
    while not game_over:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Player movement
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_height:
            player_y += player_speed

        # Shooting bullets
        if keys[pygame.K_SPACE]:
            bullet = pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height)
            bullets.append(bullet)

        # Update bullet positions
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Spawn enemies
        if random.randint(1, 50) == 1:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemies.append(pygame.Rect(enemy_x, 0, enemy_width, enemy_height))

        # Update enemy positions
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)

        # Check for collisions (bullet hits enemy)
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    enemies.remove(enemy)
                    bullets.remove(bullet)

        # Draw everything
        draw_player(player_x, player_y)
        for bullet in bullets:
            draw_bullet(bullet         )
        for enemy in enemies:
            draw_enemy(enemy)

        # Display game over text if necessary
        for enemy in enemies:
            if enemy.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                game_over = True
                game_over_text = font.render("Game Over! Press Q to Quit.", True, BLACK)
                screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        clock.tick(2000)  # 60 FPS

# Start the game
game_loop()

# Quit Pygame
pygame.quit()
sys.exit()
