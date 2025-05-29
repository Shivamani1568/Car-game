import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Car settings
car_width, car_height = 50, 100
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 20
car_speed = 5

# Obstacle settings
obs_width, obs_height = 50, 100
obs_speed = 5
obstacles = []

# Font
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# Score
score = 0

def draw_car(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, car_width, car_height))

def draw_obstacle(obs):
    pygame.draw.rect(screen, RED, obs)

def show_text(text, size, color, y_offset=0):
    font_used = big_font if size == 'big' else font
    text_surf = font_used.render(text, True, color)
    text_rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surf, text_rect)

def game_over_screen():
    show_text("You Crashed!", 'big', RED, -40)
    show_text("Press C to Continue or Q to Quit", 'small', WHITE, 40)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    main_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main_game():
    global car_x, obstacles, score

    car_x = WIDTH // 2 - car_width // 2
    obstacles = []
    score = 0
    frame_count = 0

    running = True
    while running:
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width:
            car_x += car_speed

        # Generate obstacles
        if frame_count % 60 == 0:
            obs_x = random.randint(0, WIDTH - obs_width)
            obstacles.append(pygame.Rect(obs_x, -obs_height, obs_width, obs_height))

        # Move and draw obstacles
        for obs in obstacles[:]:
            obs.y += obs_speed
            draw_obstacle(obs)
            if obs.colliderect(pygame.Rect(car_x, car_y, car_width, car_height)):
                game_over_screen()
            if obs.y > HEIGHT:
                obstacles.remove(obs)
                score += 1

        draw_car(car_x, car_y)

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)
        frame_count += 1

# Start the game
main_game()
