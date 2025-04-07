import pygame
import os
from network import Network

# Initialize pygame modules
pygame.font.init()
pygame.mixer.init()

# Game window setup
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Battle - Online")

# Define colors using RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create game elements
# Center dividing line
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
# Fonts for displaying text
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
STATUS_FONT = pygame.font.SysFont('comicsans', 30)

# Game constants
FPS = 60  # Frames per second (game update rate)
VEL = 5   # Velocity/speed of spaceship movement
BULLET_VEL = 7  # Speed of bullets
MAX_BULLETS = 3  # Maximum number of bullets each player can have
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40  # Dimensions for spaceship images

# Add GameState class definition to match the server's definition
class GameState:
    def __init__(self):
        # Initial positions of the red and yellow spaceships
        self.red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        
        # Lists to hold bullets for each player
        self.red_bullets = []
        self.yellow_bullets = []
        
        # Initial health for each player
        self.red_health = 10
        self.yellow_health = 10
        
        # Game status
        self.winner = ""
        self.ready = False

# Load and transform spaceship images
# Yellow spaceship (left side player)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
# Scale and rotate the image to face right
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Red spaceship (right side player)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
# Scale and rotate the image to face left
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Load and scale background image
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(game_state, player_id):
    # Draw background
    WIN.blit(SPACE, (0, 0))
    # Draw center dividing line
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Draw health indicators for both players
    red_health_text = HEALTH_FONT.render("Health: " + str(game_state.red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(game_state.yellow_health), 1, WHITE)
    # Position health text in top corners
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Draw spaceships at their current positions
    WIN.blit(YELLOW_SPACESHIP, (game_state.yellow.x, game_state.yellow.y))
    WIN.blit(RED_SPACESHIP, (game_state.red.x, game_state.red.y))

    # Draw all bullets
    # Red bullets are drawn as red rectangles
    for bullet in game_state.red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    # Yellow bullets are drawn as yellow rectangles
    for bullet in game_state.yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # Draw indicator showing which player you are
    if player_id == 0:
        player_text = STATUS_FONT.render("You are: Yellow", 1, YELLOW)
    else:
        player_text = STATUS_FONT.render("You are: Red", 1, RED)
    # Position player indicator at bottom center
    WIN.blit(player_text, (WIDTH//2 - player_text.get_width()//2, HEIGHT - 40))

    # Draw waiting message if game is not ready (waiting for second player)
    if not game_state.ready:
        waiting_text = STATUS_FONT.render("Waiting for other player...", 1, WHITE)
        WIN.blit(waiting_text, (WIDTH//2 - waiting_text.get_width()//2, HEIGHT//2))

    # Draw winner text if there is a winner
    if game_state.winner != "":
        draw_winner(game_state.winner)

    # Update the display to show all drawn elements
    pygame.display.update()

def draw_winner(text):
    # Render winner text
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    # Position winner text in center of screen
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2,
                         HEIGHT/2 - draw_text.get_height()/2))
    # Update display to show winner text
    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow):
    # Move left if 'A' is pressed and not at left edge
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    # Move right if 'D' is pressed and not at border
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    # Move up if 'W' is pressed and not at top edge
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    # Move down if 'S' is pressed and not at bottom edge
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL
    return yellow

def handle_red_movement(keys_pressed, red):
    # Move left if left arrow is pressed and not at border
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    # Move right if right arrow is pressed and not at right edge
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    # Move up if up arrow is pressed and not at top edge
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    # Move down if down arrow is pressed and not at bottom edge
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL
    return red

def main():
    # Create network connection to server
    # This initializes the socket and connects to the server
    n = Network()
    
    # Get player ID from server (0 for yellow, 1 for red)
    player_id = n.player_id
    
    # Check if connection was successful
    if player_id is None:
        print("Couldn't connect to server!")
        return
    
    print(f"You are player {player_id}")
    
    # Get initial game state from server
    # This is the first communication after getting player ID
    game_state = n.send({"position": pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) if player_id == 0 
                         else pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT), 
                         "new_bullet": False})
    
    # Game loop setup
    clock = pygame.time.Clock()
    run = True
    
    # Flag to track if player fired a bullet this frame
    new_bullet = False
    
    # Main game loop
    while run:
        # Limit game to run at specified FPS
        clock.tick(FPS)
        
        # Send current player state to server and get updated game state
        # This happens every frame - the client sends its current position
        # and whether it fired a bullet, then receives the complete game state
        game_state = n.send({"position": game_state.yellow if player_id == 0 else game_state.red, 
                             "new_bullet": new_bullet})
        # Reset bullet firing flag after sending
        new_bullet = False
        
        # Process pygame events (key presses, window close, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            # Handle bullet firing based on player ID
            if event.type == pygame.KEYDOWN:
                # Yellow player fires with left control
                if player_id == 0 and event.key == pygame.K_LCTRL:
                    new_bullet = True
                # Red player fires with space
                elif player_id == 1 and event.key == pygame.K_SPACE:
                    new_bullet = True
        
        # Get currently pressed keys for movement
        keys_pressed = pygame.key.get_pressed()
        
        # Handle movement based on player ID
        if player_id == 0:  # Yellow player
            # Update yellow spaceship position based on key presses
            my_rect = handle_yellow_movement(keys_pressed, game_state.yellow)
        else:  # Red player
            # Update red spaceship position based on key presses
            my_rect = handle_red_movement(keys_pressed, game_state.red)
        
        # Draw game with current game state
        draw_window(game_state, player_id)

# Entry point of the script
if __name__ == "__main__":
    main()