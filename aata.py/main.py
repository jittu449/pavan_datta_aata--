import pygame
import random
import asyncio

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy You")

clock = pygame.time.Clock()

# Colors
BLUE = (135, 206, 250)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Bird
bird_img = pygame.image.load("Auraa.jpeg").convert_alpha()
bird_img = pygame.transform.scale(bird_img, (40, 40))

bird_x = 80
bird_y = HEIGHT // 2
gravity = 0.5
velocity = 0
jump_power = -10

# Sounds (safe loading)
try:
    jump_sound = pygame.mixer.Sound("jump.wav.mpeg")
    hit_sound = pygame.mixer.Sound("hit.wave.mpeg")
except:
    jump_sound = None
    hit_sound = None

# Pipes
pipe_width = 70
pipe_gap = 170
pipe_x = WIDTH
pipe_height = random.randint(120, 400)
pipe_speed = 3

score = 0
font = pygame.font.SysFont("Arial", 32)

def draw_pipes():
    top_rect = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    bottom_rect = pygame.Rect(
        pipe_x,
        pipe_height + pipe_gap,
        pipe_width,
        HEIGHT - pipe_height - pipe_gap
    )
    pygame.draw.rect(screen, GREEN, top_rect)
    pygame.draw.rect(screen, GREEN, bottom_rect)
    return top_rect, bottom_rect


async def main():
    global velocity, bird_y, pipe_x, pipe_height, score

    running = True

    while running:
        clock.tick(60)
        screen.fill(BLUE)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    velocity = jump_power
                    if jump_sound:
                        jump_sound.play()

        # Bird physics
        velocity += gravity
        bird_y += velocity

        angle = -velocity * 3
        rotated_bird = pygame.transform.rotate(bird_img, angle)
        bird_rect = rotated_bird.get_rect(center=(bird_x, bird_y))

        # Move pipes
        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(120, 400)
            score += 1

        # Draw pipes
        top_rect, bottom_rect = draw_pipes()
        screen.blit(rotated_bird, bird_rect.topleft)

        # Score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Collision
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            if hit_sound:
                hit_sound.play()
            running = False

        if bird_y <= 0 or bird_y >= HEIGHT:
            if hit_sound:
                hit_sound.play()
            running = False

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())