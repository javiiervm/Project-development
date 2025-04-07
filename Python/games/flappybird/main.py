import pygame
import os
import random

# Initializing the font and mixer modules of pygame
pygame.font.init()
pygame.mixer.init()

# Setting up window dimensions and creating the game window
WIDTH, HEIGHT = 850, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy bird 🐦")

FPS = 60
VEL = 3
JUMP_VELOCITY = 50
GRAVITY = VEL/2
PIPEVEL = 2
BIRDWIDTH, BIRDHEIGHT = 50,35
MINPIPEHEIGHT, MAXPIPEHEIGHT = 400, 100
GAP = BIRDHEIGHT + 4  *(BIRDHEIGHT//2)
PIPE_GAP = 200

BIRD_JUMP = pygame.USEREVENT + 1

# Images
BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "background.png"))
SCALED_BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
BIRD = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bird.png")), (BIRDWIDTH,BIRDHEIGHT))
PIPE = pygame.image.load(os.path.join("Assets", "FullPipe.png"))
MIRRORPIPE = pygame.image.load(os.path.join("Assets", "MirrorPipe.png"))

def pipeGenerator():
    inferiorlimit = random.randint(100, HEIGHT - 100 - GAP)
    pipe_down_y = HEIGHT - inferiorlimit
    pipe_up_y = pipe_down_y - GAP - PIPE.get_height()
    return pipe_down_y, pipe_up_y

def handle_pipes(pipelist):
    for i in range(len(pipelist)):
        pipe_rect, down = pipelist[i]
        pipe_rect.x -= PIPEVEL
        pipelist[i] = (pipe_rect, down)

    if pipelist:
        if pipelist[0][0].x < (0 - PIPE.get_width()):
            pipelist.pop(0)
        last_element = pipelist[-1][0]
        if last_element.x < WIDTH - PIPE_GAP:
            pipe_down_y, pipe_up_y = pipeGenerator()
            pipe_down = pygame.Rect(WIDTH, pipe_down_y, PIPE.get_width(), PIPE.get_height())
            pipe_up = pygame.Rect(WIDTH, pipe_up_y, PIPE.get_width(), PIPE.get_height())
            pipelist.append((pipe_down, True))
            pipelist.append((pipe_up, False))
    else:
        pipe_down_y, pipe_up_y = pipeGenerator()
        pipe_down = pygame.Rect(WIDTH, pipe_down_y, PIPE.get_width(), PIPE.get_height())
        pipe_up = pygame.Rect(WIDTH, pipe_up_y, PIPE.get_width(), PIPE.get_height())
        pipelist.append((pipe_down, True))
        pipelist.append((pipe_up, False))

def bird_jump(keys_pressed, bird, has_jumped):
    if keys_pressed[pygame.K_SPACE] and bird.y - JUMP_VELOCITY > 0 and not has_jumped:
        has_jumped = True
        pygame.event.post(pygame.event.Event(BIRD_JUMP))
    if not keys_pressed[pygame.K_SPACE] and has_jumped:
        has_jumped = False
    return has_jumped

def apply_gravity(bird):
    bird.y += GRAVITY

def check_collision(bird, pipelist):
    for pipe_rect, _ in pipelist:
        if bird.colliderect(pipe_rect):
            return True
    return False

def draw_window(bird, pipelist):
    WIN.blit(SCALED_BACKGROUND, (0,0))
    WIN.blit(BIRD, (bird.x, bird.y))

    for i in range (len(pipelist)):
        value, down = pipelist[i]
        if down:
            WIN.blit(PIPE, (value.x, value.y))
        else:
            WIN.blit(pygame.transform.rotate(MIRRORPIPE, 180), (value.x, value.y))

    # Updates the display with all the drawn elements
    pygame.display.update()

def main():
    bird = pygame.Rect(100, HEIGHT//2, BIRDWIDTH, BIRDHEIGHT)
    pipelist = []
    has_jumped = False
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == BIRD_JUMP:
                bird.y -= JUMP_VELOCITY

        keys_pressed = pygame.key.get_pressed()
        has_jumped = bird_jump(keys_pressed, bird, has_jumped)
        apply_gravity(bird)
        handle_pipes(pipelist)

        if check_collision(bird, pipelist):
            print("Collision")
            run = False

        draw_window(bird, pipelist)

if __name__ == "__main__":
    main()