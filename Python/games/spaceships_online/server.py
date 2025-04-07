import socket
import pickle
import pygame
import threading
from _thread import start_new_thread

# Import game constants from main.py
from main import WIDTH, HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, BULLET_VEL, MAX_BULLETS

# Server setup
# "0.0.0.0" means listen on all available network interfaces
# This allows connections from other computers, not just localhost
server = "0.0.0.0"  
port = 5555

# Create a TCP socket object for the server
# AF_INET indicates we're using IPv4
# SOCK_STREAM indicates we're using TCP (reliable, ordered data stream)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Bind the socket to the specified IP and port
    # This reserves the port for our server application
    s.bind((server, port))
except socket.error as e:
    # Print any errors that occur during binding
    print(str(e))

# Start listening for incoming connections
# The argument (2) specifies the maximum number of queued connections
s.listen(2)  # Only allow 2 connections (2 players)
print("Server started, waiting for connections...")

# Game state class to store and manage all game data
class GameState:
    def __init__(self):
        # Initial positions of the red and yellow spaceships
        # pygame.Rect objects store position and size information
        self.red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        
        # Lists to hold bullets for each player
        # Each bullet will be a pygame.Rect object
        self.red_bullets = []
        self.yellow_bullets = []
        
        # Initial health for each player
        self.red_health = 10
        self.yellow_health = 10
        
        # Game status flags
        self.winner = ""  # Empty string means no winner yet
        self.ready = False  # Game starts when both players are connected

# Create a single game state instance that will be shared between all clients
game_state = GameState()

# Create a threading lock to prevent race conditions when multiple threads
# try to modify the game state simultaneously
lock = threading.Lock()

def handle_client(conn, player):
    # Send the player ID to the client (0 for yellow, 1 for red)
    # pickle.dumps serializes the Python object to a byte stream
    conn.send(pickle.dumps(player))
    
    # Main client handling loop - runs continuously while client is connected
    while True:
        try:
            # Receive data from client (player position and bullet firing info)
            # recv(2048) reads up to 2048 bytes from the client
            # pickle.loads deserializes the byte stream back to a Python object
            data = pickle.loads(conn.recv(2048))
            
            # Acquire the lock to safely modify the shared game state
            # This prevents other threads from modifying the game state simultaneously
            with lock:
                # Update game state based on player input
                if player == 0:  # Yellow player
                    # Update yellow spaceship position
                    game_state.yellow = data["position"]
                    
                    # Check if player fired a new bullet
                    if "new_bullet" in data and data["new_bullet"]:
                        # Create a new bullet rectangle at the appropriate position
                        bullet = pygame.Rect(
                            game_state.yellow.x + game_state.yellow.width, 
                            game_state.yellow.y + game_state.yellow.height//2 - 2, 
                            10, 5)
                        # Add the bullet to the yellow player's bullets list
                        game_state.yellow_bullets.append(bullet)
                
                elif player == 1:  # Red player
                    # Update red spaceship position
                    game_state.red = data["position"]
                    
                    # Check if player fired a new bullet
                    if "new_bullet" in data and data["new_bullet"]:
                        # Create a new bullet rectangle at the appropriate position
                        bullet = pygame.Rect(
                            game_state.red.x, 
                            game_state.red.y + game_state.red.height//2 - 2, 
                            10, 5)
                        # Add the bullet to the red player's bullets list
                        game_state.red_bullets.append(bullet)
                
                # Send the updated game state back to the client
                # pickle.dumps serializes the game state object to a byte stream
                # sendall ensures all data is sent in one go
                conn.sendall(pickle.dumps(game_state))
                
            # If both players are connected and the game isn't already running,
            # start the game update thread
            if len(connected) == 2 and not game_state.ready:
                game_state.ready = True
                # Start a new thread to handle game logic updates
                # This allows the server to continue handling client connections
                # while also updating the game state
                start_new_thread(update_game, ())
                
        except:
            # If any error occurs (usually client disconnection), break the loop
            break
    
    # Client disconnected - clean up
    print(f"Lost connection to player {player}")
    try:
        # Remove the player from the connected dictionary
        del connected[player]
        # Close the connection socket
        conn.close()
    except:
        # Handle any errors during cleanup
        pass

def update_game():
    # Create a clock to control the game update rate
    clock = pygame.time.Clock()
    
    # Main game update loop - runs continuously
    while True:
        # Limit the loop to run at 60 iterations per second
        # This matches the client's frame rate
        clock.tick(60)
        
        # Acquire the lock to safely modify the shared game state
        with lock:
            if game_state.ready:
                # Update yellow bullets positions and check for collisions
                # Using [:] creates a copy of the list so we can safely modify
                # the original list while iterating
                for bullet in game_state.yellow_bullets[:]:
                    # Move bullet to the right
                    bullet.x += BULLET_VEL
                    
                    # Check if bullet hits red spaceship
                    if game_state.red.colliderect(bullet):
                        # Reduce red player's health
                        game_state.red_health -= 1
                        # Remove the bullet
                        game_state.yellow_bullets.remove(bullet)
                    # Check if bullet goes off-screen
                    elif bullet.x > WIDTH:
                        # Remove the bullet
                        game_state.yellow_bullets.remove(bullet)
                
                # Update red bullets positions and check for collisions
                for bullet in game_state.red_bullets[:]:
                    # Move bullet to the left
                    bullet.x -= BULLET_VEL
                    
                    # Check if bullet hits yellow spaceship
                    if game_state.yellow.colliderect(bullet):
                        # Reduce yellow player's health
                        game_state.yellow_health -= 1
                        # Remove the bullet
                        game_state.red_bullets.remove(bullet)
                    # Check if bullet goes off-screen
                    elif bullet.x < 0:
                        # Remove the bullet
                        game_state.red_bullets.remove(bullet)
                
                # Check for winner based on health
                if game_state.red_health <= 0:
                    game_state.winner = "Yellow Wins!"
                
                if game_state.yellow_health <= 0:
                    game_state.winner = "Red Wins!"
                
                # Reset game if there's a winner
                if game_state.winner != "":
                    # Wait 5 seconds before resetting the game
                    # This gives players time to see who won
                    pygame.time.delay(5000)
                    
                    # Reset game state for a new round
                    game_state.red_health = 10
                    game_state.yellow_health = 10
                    game_state.red_bullets = []
                    game_state.yellow_bullets = []
                    game_state.winner = ""

# Dictionary to store connected clients
# Keys are player IDs (0 or 1), values are connection objects
connected = {}

# Counter to track how many players have connected
player_count = 0

# Main server loop - continuously accepts new connections
while True:
    # accept() waits for a new connection and returns a new socket object
    # and the address (IP, port) of the client
    # This is a blocking call - it waits until a client connects
    conn, addr = s.accept()
    print(f"Connected to: {addr}")
    
    # Assign player number (0 for yellow, 1 for red)
    # Only allow up to 2 players
    if player_count < 2:
        # Store the connection in the connected dictionary
        connected[player_count] = conn
        
        # Start a new thread to handle this client
        # This allows the server to handle multiple clients simultaneously
        # Each client gets its own thread for communication
        start_new_thread(handle_client, (conn, player_count))
        
        # Increment player count for the next connection
        player_count += 1