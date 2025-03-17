import pygame
import random
import os

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, HEIGHT // 2
BIRD_RADIUS = 15
gravity = 0.5
jump_strength = -8
pipe_width = 70
gap_height = 150
pipe_speed = 4
score = 0
best_score = 0

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

lives = 3

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
def load_bird_sprites(color):
    return [
        pygame.image.load(os.path.join(BASE_DIR, "images", f"{color}bird-downflap.png")).convert_alpha(),
        pygame.image.load(os.path.join(BASE_DIR, "images", f"{color}bird-midflap.png")).convert_alpha(),
        pygame.image.load(os.path.join(BASE_DIR, "images", f"{color}bird-upflap.png")).convert_alpha(),
    ]

# Load background for menus
menu_background = pygame.image.load(os.path.join(BASE_DIR, "images", "fondo.jpg")).convert()
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

def show_start_menu():
    screen.blit(menu_background, (0, 0))
    font = pygame.font.Font(pygame.font.match_font('PressStart2P', True), 24)
    
    # Game title
    title_text = font.render("Flappy-ish Bird", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    screen.blit(title_text, title_rect)
    
    # Start message
    start_text = font.render("Press ENTER to Start", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(start_text, start_rect)
    
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

def show_bird_selection_menu():
    screen.blit(menu_background, (0, 0))
    font = pygame.font.Font(pygame.font.match_font('PressStart2P', True), 24)
    text = font.render("Press B for Blue Bird", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
    screen.blit(text, text_rect)
    
    text = font.render("Press Y for Yellow Bird", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    
    text = font.render("Press R for Red Bird", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
    screen.blit(text, text_rect)
    
    pygame.display.update()
    waiting = True
    selected_color = None
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    selected_color = "blue"
                    waiting = False
                if event.key == pygame.K_y:
                    selected_color = "yellow"
                    waiting = False
                if event.key == pygame.K_r:
                    selected_color = "red"
                    waiting = False
    return selected_color

# Show start menu before the game begins
show_start_menu()

# Show bird selection menu before the game begins
selected_color = show_bird_selection_menu()
bird_images = load_bird_sprites(selected_color)

# Randomly choose between day and night background
background_choice = random.choice(["background-day.png", "background-night.png"])
background = pygame.image.load(os.path.join(BASE_DIR, "images", background_choice)).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

ground_image = pygame.image.load(os.path.join(BASE_DIR, "images", "base.png")).convert_alpha()
ground_image = pygame.transform.scale(ground_image, (WIDTH, ground_image.get_height()))

# Randomly choose between green and red pipes
pipe_choice = random.choice(["pipe-green.png", "pipe-red.png"])
pipe_image = pygame.image.load(os.path.join(BASE_DIR, "images", pipe_choice)).convert_alpha()
pipe_image_flipped = pygame.transform.flip(pipe_image, False, True)

# Clock for frame rate
clock = pygame.time.Clock()

# Game State
game_started = False
playing = True

# Bird attributes
bird_y = BIRD_Y
bird_velocity = 0
bird_frame = 0

# Pipe attributes
pipes = []

def reset_bird():
    global best_score
    if score > best_score:
        best_score = score
    global bird_y, bird_velocity, pipes
    bird_y = BIRD_Y
    bird_velocity = 0
    pipes.clear()

def check_collision():
    global lives, bird_y, bird_velocity, pipes

    if bird_y - BIRD_RADIUS <= 0 or bird_y + BIRD_RADIUS >= HEIGHT:
        lives -= 1
        reset_bird()
        return lives <= 0  
    
    for pipe in pipes:
        if BIRD_X + BIRD_RADIUS > pipe[0] and BIRD_X - BIRD_RADIUS < pipe[0] + pipe_width:
            if bird_y - BIRD_RADIUS < pipe[1] or bird_y + BIRD_RADIUS > pipe[1] + gap_height:
                lives -= 1
                reset_bird()
                return lives <= 0  
    return False

# Game loop
running = True
frame_count = 0

while running:
    screen.blit(background, (0, 0))
    screen.blit(ground_image, (0, HEIGHT - ground_image.get_height()))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength
            if event.key == pygame.K_p:
                playing = not playing  
    
    if playing:
        bird_velocity += gravity
        bird_y += bird_velocity
        
        if frame_count % 90 == 0:
            pipes.append([WIDTH, random.randint(50, HEIGHT - gap_height - 50), random.choice([-1, 1])])
        
        for pipe in pipes:
            pipe[0] -= pipe_speed
        
        for pipe in pipes[:]:
            if pipe[0] + pipe_width < 0:
                pipes.remove(pipe)
                score += 1  
        
        for pipe in pipes:
            screen.blit(pygame.transform.scale(pipe_image_flipped, (pipe_width, pipe[1])), (pipe[0], 0))
            screen.blit(pygame.transform.scale(pipe_image, (pipe_width, HEIGHT - (pipe[1] + gap_height))), (pipe[0], pipe[1] + gap_height))
        
        bird_frame = (bird_frame + 1) % len(bird_images)  
        screen.blit(bird_images[bird_frame], (BIRD_X - BIRD_RADIUS, int(bird_y - BIRD_RADIUS)))
        
        font = pygame.font.Font(pygame.font.match_font('PressStart2P', True), 24)
        text = font.render(f"Score: {score}  Best: {best_score}", True, (255, 215, 0))
        screen.blit(text, (10, 10))
        
        text = font.render(f"Lives: {lives}", True, (255, 255, 0))  # Yellow color
        screen.blit(text, (WIDTH - 100, 10))
        
        if check_collision():
            if lives <= 0:
                font = pygame.font.Font(pygame.font.match_font('PressStart2P', True), 24)
                text = font.render('Game Over! Press R to Restart', True, (255, 255, 0))  # Yellow color
                score_text = font.render(f'Your Score: {score}', True, (255, 255, 0))  # Yellow color
                best_text = font.render(f'Best Score: {best_score}', True, (255, 255, 0))  # Yellow color
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
                score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                best_rect = best_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
                screen.blit(text, text_rect)
                screen.blit(score_text, score_rect)
                screen.blit(best_text, best_rect)
                pygame.display.update()
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            lives = 3
                            score = 0
                            reset_bird()
                            waiting = False
    else:
        screen.blit(menu_background, (0, 0))
        font = pygame.font.Font(pygame.font.match_font('PressStart2P', True), 24)
        text = font.render("Game Paused", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        screen.blit(text, text_rect)
        
        text = font.render("Press P to Resume", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(text, text_rect)
        
        pygame.display.update()
    
    frame_count += 1
    pygame.display.update()
    clock.tick(30)

pygame.quit()
