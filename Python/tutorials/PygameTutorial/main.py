# Importing the pygame module and os for file path handling
import pygame
import os

# Initializing the font and mixer modules of pygame (mixer is used for sound)
pygame.font.init()
pygame.mixer.init()

# Setting up window dimensions and creating the game window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")  # Sets the title of the game window

# Defining colors using RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Creating a vertical border at the center of the screen to separate the two players
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# Loading sound effects (currently commented out because files may not be found or playable)
# These lines load sound effects from the Assets folder.
# BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
# BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

# Setting up fonts for displaying player health and the winner announcement
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)  # Font for health display
WINNER_FONT = pygame.font.SysFont('comicsans', 100)  # Font for displaying winner text

# Game constants
FPS = 60  # Frames per second
VEL = 5  # Velocity/speed of spaceship movement
BULLET_VEL = 7  # Speed of bullets
MAX_BULLETS = 3  # Maximum number of bullets each player can have on screen at once
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40  # Dimensions for spaceship images

# Creating custom user events for when each spaceship is hit
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Loading and transforming the yellow spaceship image
# Rotated 90 degrees to face right
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

# Loading and transforming the red spaceship image
# Rotated 270 degrees to face left
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# Loading and scaling the background image to match the window size
SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


# Function to draw all game elements each frame
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))  # Draws background
    pygame.draw.rect(WIN, BLACK, BORDER)  # Draws the center dividing line

    # Renders and places the health values for each player
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # Draws the spaceships
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # Draws the bullets currently on screen
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # Updates the display with all the drawn elements
    pygame.display.update()


# Handles movement of the yellow spaceship using WASD keys
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # Move left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # Move right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # Move up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # Move down
        yellow.y += VEL


# Handles movement of the red spaceship using arrow keys
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # Move left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # Move right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # Move up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # Move down
        red.y += VEL


# Handles bullet movement and collision detection
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL  # Moves bullet to the right
        if red.colliderect(bullet):  # Checks if bullet hits red spaceship
            pygame.event.post(pygame.event.Event(RED_HIT))  # Triggers RED_HIT event
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:  # Removes bullets that go off-screen
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL  # Moves bullet to the left
        if yellow.colliderect(bullet):  # Checks if bullet hits yellow spaceship
            pygame.event.post(pygame.event.Event(YELLOW_HIT))  # Triggers YELLOW_HIT event
            red_bullets.remove(bullet)
        elif bullet.x < 0:  # Removes bullets that go off-screen
            red_bullets.remove(bullet)


# Displays the winner text in the center of the screen
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2,
                         HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)  # Pause for 5 seconds before restarting


# Main game loop
def main():
    # Initial positions of the red and yellow spaceships using pygame.Rect
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # Lists to hold bullets for each player
    red_bullets = []
    yellow_bullets = []

    # Initial health for each player
    red_health = 10
    yellow_health = 10

    # Game loop setup
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)  # Ensures the game runs at a consistent FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If window is closed
                run = False
                pygame.quit()

            # Handles key presses for shooting bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    # Creates new bullet from yellow spaceship
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()  # Would play sound if un-commented

                if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    # Creates new bullet from red spaceship
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # BULLET_FIRE_SOUND.play()  # Would play sound if un-commented

            # Handles custom hit events
            if event.type == RED_HIT:
                red_health -= 1  # Red loses health
                # BULLET_HIT_SOUND.play()  # Would play sound if un-commented

            if event.type == YELLOW_HIT:
                yellow_health -= 1  # Yellow loses health
                # BULLET_HIT_SOUND.play()  # Would play sound if un-commented

        # Determines if the game has ended
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"  # Yellow wins if red health is 0

        if yellow_health <= 0:
            winner_text = "Red Wins!"  # Red wins if yellow health is 0

        if winner_text != "":
            draw_winner(winner_text)  # Display the winner and break loop
            break

        # Get currently pressed keys for movement
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        # Update bullet positions and handle collisions
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # Redraw everything on the screen
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    # Restarts the game after someone wins
    main()


# Entry point of the script
if __name__ == "__main__":
    main()
