import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bird
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipes
PIPE_WIDTH = 60
PIPE_HEIGHT = 400
PIPE_GAP = 150
pipe_velocity = -5
pipe_x = WIDTH
pipe_y = random.randint(100, HEIGHT - PIPE_GAP - 100)

# Score
score = 0
font = pygame.font.Font(None, 36)

def draw_bird():
    pygame.draw.rect(SCREEN, RED, (bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT))

def draw_pipe(x, y):
    pygame.draw.rect(SCREEN, BLACK, (x, 0, PIPE_WIDTH, y))
    pygame.draw.rect(SCREEN, BLACK, (x, y + PIPE_GAP, PIPE_WIDTH, HEIGHT))

def check_collision():
    if bird_y + BIRD_HEIGHT > HEIGHT or bird_y < 0:
        return True
    if (bird_x + BIRD_WIDTH > pipe_x and bird_x < pipe_x + PIPE_WIDTH):
        if bird_y < pipe_y or bird_y + BIRD_HEIGHT > pipe_y + PIPE_GAP:
            return True
    return False

def update_score():
    global score
    if pipe_x + PIPE_WIDTH < bird_x and pipe_x + PIPE_WIDTH + pipe_velocity >= bird_x:
        score += 1

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

    # Bird movement
    bird_velocity += gravity
    bird_y += bird_velocity

    # Pipe movement
    pipe_x += pipe_velocity
    if pipe_x < -PIPE_WIDTH:
        pipe_x = WIDTH
        pipe_y = random.randint(100, HEIGHT - PIPE_GAP - 100)

    # Check collision
    if check_collision():
        running = False

    # Update score
    update_score()

    # Draw everything
    SCREEN.fill(WHITE)
    draw_bird()
    draw_pipe(pipe_x, pipe_y)
    score_text = font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
