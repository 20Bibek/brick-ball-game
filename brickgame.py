import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 120, 20
BALL_RADIUS = 15
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BUTTON_WIDTH, BUTTON_HEIGHT = 120, 50
FPS = 60

# Colors
BACKGROUND_COLOR = (0, 0, 0)
PADDLE_COLOR = (0, 128, 255)  # Roblox blue
BALL_COLOR = (255, 255, 255)
BRICK_COLOR = (255, 255, 0)  # Yellow
GAME_OVER_COLOR = (255, 0, 0)
BUTTON_COLOR = (0, 255, 0)  # Roblox green
BUTTON_HOVER_COLOR = (0, 200, 0)  # Darker green for hover effect
BUTTON_CLICK_COLOR = (0, 150, 0)  # Even darker green for click effect
BUTTON_SHADOW_COLOR = (0, 100, 0)  # Darkest green for shadow effect
GLOW_COLOR = (255, 255, 0)  # Yellow for glow effect

# Font
GAME_OVER_FONT = pygame.font.Font(None, 50)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Initialize paddle and ball positions
paddle_width_half = PADDLE_WIDTH // 2
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 5 * random.choice([1, -1])
ball_speed_y = 5

# Create bricks
bricks = []
for row in range(5):
    for col in range(WIDTH // BRICK_WIDTH):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# Game state
game_over = False

# Function to restart the game
def restart_game():
    global game_over, paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, bricks
    game_over = False
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = 5 * random.choice([1, -1])
    ball_speed_y = 5
    bricks = [pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT, BRICK_WIDTH, BRICK_HEIGHT) 
              for row in range(5) for col in range(WIDTH // BRICK_WIDTH)]

# Restart and Quit buttons
restart_button = pygame.Rect(WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)
quit_button = pygame.Rect(3 * WIDTH // 4 - BUTTON_WIDTH // 2, HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the restart button is clicked
            if game_over and restart_button.collidepoint(event.pos):
                restart_game()
            # Check if the quit button is clicked
            elif game_over and quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

    # Get mouse position for paddle control
    mouse_x, _ = pygame.mouse.get_pos()
    paddle_x = mouse_x - paddle_width_half

    # Update button colors for hover effect
    restart_button_color = BUTTON_HOVER_COLOR if restart_button.collidepoint(mouse_x, _ ) else BUTTON_COLOR
    quit_button_color = BUTTON_HOVER_COLOR if quit_button.collidepoint(mouse_x, _ ) else BUTTON_COLOR

    # Update button colors for click effect
    if game_over:
        if restart_button.collidepoint(mouse_x, _ ) and pygame.mouse.get_pressed()[0]:
            restart_button_color = BUTTON_CLICK_COLOR
        if quit_button.collidepoint(mouse_x, _ ) and pygame.mouse.get_pressed()[0]:
            quit_button_color = BUTTON_CLICK_COLOR

    # Update button colors for shadow effect
    restart_button_shadow_color = BUTTON_SHADOW_COLOR if restart_button.collidepoint(mouse_x, _ ) else restart_button_color
    quit_button_shadow_color = BUTTON_SHADOW_COLOR if quit_button.collidepoint(mouse_x, _ ) else quit_button_color

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball collisions with walls
    if ball_x - BALL_RADIUS < 0 or ball_x + BALL_RADIUS > WIDTH:
        ball_speed_x = -ball_speed_x
    if ball_y - BALL_RADIUS < 0:
        ball_speed_y = -ball_speed_y

    # Check if the ball missed the paddle
    if ball_y + BALL_RADIUS > HEIGHT:
        game_over = True

    # Ball collision with paddle
    if (
        paddle_x < ball_x < paddle_x + PADDLE_WIDTH
        and paddle_y < ball_y < paddle_y + PADDLE_HEIGHT
    ):
        ball_speed_y = -ball_speed_y

    # Ball collision with bricks
    for brick in bricks:
        if brick.colliderect(pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, BRICK_COLOR, brick)

    # Draw paddle with rounded corners
    pygame.draw.rect(screen, PADDLE_COLOR, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT), border_radius=10)

    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Draw "Game Over" message at the center
    if game_over:
        game_over_text = GAME_OVER_FONT.render("Game Over", True, GAME_OVER_COLOR)
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(game_over_text, text_rect)

        # Draw Restart button
        pygame.draw.rect(screen, restart_button_shadow_color, (restart_button.x + 5, restart_button.y + 5, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, restart_button_color, restart_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Restart", True, BACKGROUND_COLOR)
        text_rect = text.get_rect(center=restart_button.center)
        screen.blit(text, text_rect)

        # Draw Quit button
        pygame.draw.rect(screen, quit_button_shadow_color, (quit_button.x + 5, quit_button.y + 5, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, quit_button_color, quit_button)
        text = font.render("Quit", True, BACKGROUND_COLOR)
        text_rect = text.get_rect(center=quit_button.center)
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
