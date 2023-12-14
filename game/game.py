import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT_SIZE = 36
BULLETS_TO_DESTROY_SMALL = 5
BULLETS_TO_DESTROY_LARGE = 10

# Load background image
background_image = pygame.image.load("./assets/space.jpg")  # Replace "background.jpg" with the actual file path of your background image
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


# Load player image
player_image = pygame.image.load("./assets/jet.jpg")
player_image = pygame.transform.scale(player_image, (50, 50))

# Player
player_rect = player_image.get_rect(topleft=(WIDTH // 2 - player_image.get_width() // 2, HEIGHT - 2 * player_image.get_height()))

# Bullets
bullet_speed = 7
bullets = []

# Enemy
enemy_speed = 2
enemies = []

# Scoring
score = 0

# Game over flag
game_over = False

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Action Game")
font = pygame.font.Font(None, FONT_SIZE)

# Function to display game over message and score
def show_game_over():
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 20))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2))

    restart_text = font.render("Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + game_over_text.get_height() + 20))
    pygame.draw.rect(screen, WHITE, restart_rect, 2)
    screen.blit(restart_text, restart_rect.topleft)

    # Check for mouse click on restart button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    if restart_rect.collidepoint(mouse_x, mouse_y) and mouse_clicked:
        restart_game()

# Function to restart the game
def restart_game():
    global game_over, player_rect, bullets, enemies, score, enemy_speed, bullet_speed
    game_over = False
    player_rect.topleft = (WIDTH // 2 - player_rect.width // 2, HEIGHT - 2 * player_rect.height)
    bullets = []
    enemies = []
    score = 0
    enemy_speed = 2
    bullet_speed = 7
    
# Function to handle collisions between bullets and enemies
def handle_bullet_enemy_collisions():
    global bullets, enemies, score

    bullets_to_remove = []

    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets_to_remove.append(bullet)

                if enemy.width <= 50:  # Small enemy
                    score += 5
                else:  # Large enemy
                    score += 10

                enemies.remove(enemy)

    # Remove bullets that collided with enemies
    bullets = [bullet for bullet in bullets if bullet not in bullets_to_remove]



# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Draw background
    screen.blit(background_image, (0, 0))

    if not game_over:
        keys = pygame.key.get_pressed()
        player_rect.x -= 5 if keys[pygame.K_LEFT] and player_rect.left > 0 else 0
        player_rect.x += 5 if keys[pygame.K_RIGHT] and player_rect.right < WIDTH else 0

        # Spawn enemies
        if random.randint(0, 100) < 3:
            enemy = pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50)
            enemies.append(enemy)

        # Move and draw enemies
        for enemy in enemies:
            enemy.y += enemy_speed
            pygame.draw.rect(screen, RED, enemy)

        # Remove enemies that go off the screen
        enemies = [enemy for enemy in enemies if enemy.y <= HEIGHT]

        # Move and draw bullets
        bullets = [bullet for bullet in bullets if bullet.y >= 0]
        for bullet in bullets:
            bullet.y -= bullet_speed
            pygame.draw.rect(screen, BLUE, bullet)

        # Check for collisions between bullets and enemies
        handle_bullet_enemy_collisions()
		
        # Check for collisions between player and enemies
        if any(player_rect.colliderect(enemy) for enemy in enemies):
            game_over = True

        # Draw the player image
        screen.blit(player_image, player_rect.topleft)

        # Shooting mechanism
        if keys[pygame.K_SPACE]:
            bullet = pygame.Rect(player_rect.centerx - 2, player_rect.y - 10, 4, 10)
            bullets.append(bullet)

        # Increase speed after every 100 points
        if score % 100 == 0 and score != 0:
            enemy_speed += 0.01
            
        # Check for the score threshold to randomly enlarge enemies
        if score >= 100:
            for enemy in enemies:
                if random.randint(0, 100) < 3:
                    enemy.width = 100
                    enemy.height = 100

    # If game over, display the "Game Over" message and score
    if game_over:
        show_game_over()

    # Display score during gameplay
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
        # Update the display
    pygame.display.flip()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Set the frame rate
    clock.tick(FPS)
