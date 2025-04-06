import pygame
import os

# Initializing the font and mixer modules of pygame
pygame.font.init()
pygame.mixer.init()

# Setting up window dimensions and creating the game window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy bird 🐦")

FPS = 60
VEL = 3
BIRDWIDTH, BIRDHEIGHT = 100,80

# Images
BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "background.png"))
SCALED_BACKGROUND = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
BIRD = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bird.png")), (BIRDWIDTH,BIRDHEIGHT))
PIPE = pygame.image.load(os.path.join("Assets", "Pipe.png"))
CUTPIPE = pygame.image.load(os.path.join("Assets", "CutPipe.png"))


def draw_window(bird):
    WIN.blit(SCALED_BACKGROUND, (0,0))
    WIN.blit(BIRD, (bird.x, bird.y))

    # Updates the display with all the drawn elements
    pygame.display.update()

def main():
    bird = pygame.Rect(100, HEIGHT//2, BIRDWIDTH, BIRDHEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # Get pressed keys

        bird.x += VEL
        bird.y += VEL

        draw_window(bird)

if __name__ == "__main__":
    main()