# client.py

import pygame
from network import Network
from game import Game

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game")

FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

def draw_window(game):
    WIN.fill((0, 0, 0))  # Clear screen
    red = pygame.Rect(game.red['x'], game.red['y'], 55, 40)
    yellow = pygame.Rect(game.yellow['x'], game.yellow['y'], 55, 40)

    pygame.draw.rect(WIN, RED, red)
    pygame.draw.rect(WIN, YELLOW, yellow)

    for bullet in game.red_bullets:
        pygame.draw.rect(WIN, RED, (bullet[0], bullet[1], 10, 5))
    for bullet in game.yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, (bullet[0], bullet[1], 10, 5))

    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    net = Network()

    player = "yellow"  # Client controls yellow
    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        # Movement input
        if keys[pygame.K_a]:
            net.send({'action': 'move', 'player': player, 'direction': 'left'})
        if keys[pygame.K_d]:
            net.send({'action': 'move', 'player': player, 'direction': 'right'})
        if keys[pygame.K_w]:
            net.send({'action': 'move', 'player': player, 'direction': 'up'})
        if keys[pygame.K_s]:
            net.send({'action': 'move', 'player': player, 'direction': 'down'})
        if keys[pygame.K_LCTRL]:
            net.send({'action': 'shoot', 'player': player})

        # Get updated game state
        game = net.send({'action': 'noop'})  # Send no-op to get game state
        if game:
            draw_window(game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

if __name__ == "__main__":
    main()
