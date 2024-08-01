import pygame
import random
import os

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

# Load images with error handling
def load_image(file_name):
    if os.path.exists(file_name):
        return pygame.image.load(file_name)
    else:
        print(f"Error: '{file_name}' not found. Please make sure the image file is in the same directory as the script.")
        pygame.quit()
        exit()

BIRD_IMG = load_image('bird.png')
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (40, 30))
PIPE_IMG = load_image('pipe.png')
PIPE_IMG = pygame.transform.scale(PIPE_IMG, (60, 400))
BG_IMG = load_image('background.png')
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))

# Bird
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
pipe_passed = False

# Score
score = 0
font = pygame.font.Font(None, 36)

def draw_bird():
    SCREEN.blit(BIRD_IMG, (bird_x, bird_y))

def draw_pipe(x, y):
    SCREEN.blit(PIPE_IMG, (x, y - PIPE_HEIGHT))
    SCREEN.blit(PIPE_IMG, (x, y + PIPE_GAP))

def check_collision():
    if bird_y + BIRD_IMG.get_height() > HEIGHT or bird_y < 0:
        return True
    if (bird_x + BIRD_IMG.get_width() > pipe_x and bird_x < pipe_x + PIPE_WIDTH):
        if bird_y < pipe_y or bird_y + BIRD_IMG.get_height() > pipe_y + PIPE_GAP:
            return True
    return False

def update_score():
    global score, pipe_passed
    if pipe_x + PIPE_WIDTH < bird_x and not pipe_passed:
        score += 1
        pipe_passed = True

def game_over():
    global score
    SCREEN.fill(WHITE)
    game_over_text = font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Score: {score}", True, BLACK)
    restart_text = font.render("Press R to Restart", True, BLACK)
    quit_text = font.render("Press Q to Quit", True, BLACK)
    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
    SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))
    SCREEN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 80))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

def main():
    global bird_y, bird_velocity, pipe_x, pipe_y, pipe_passed, score

    bird_y = HEIGHT // 2
    bird_velocity = 0
    pipe_x = WIDTH
    pipe_y = random.randint(100, HEIGHT - PIPE_GAP - 100)
    pipe_passed = False
    score = 0

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
            pipe_passed = False

        # Check collision
        if check_collision():
            game_over()

        # Update score
        update_score()

        # Draw everything
        SCREEN.blit(BG_IMG, (0, 0))
        draw_bird()
        draw_pipe(pipe_x, pipe_y)
        score_text = font.render(f"Score: {score}", True, BLACK)
        SCREEN.blit(score_text, (10, 10))

        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
 