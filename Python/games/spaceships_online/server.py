# server.py

import socket
import pickle
from game import Game

# Server settings
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ''  # Accept connections from any IP
PORT = 5555
server.bind((HOST, PORT))
server.listen()

print("Waiting for client connection...")

conn, addr = server.accept()
print("Client connected from", addr)

# Create shared game state
game = Game()

def handle_client(conn):
    while True:
        try:
            # Receive player input
            data = pickle.loads(conn.recv(4096))
            if not data:
                break

            # Handle movement or shooting
            if data['action'] == 'move':
                game.move_player(data['player'], data['direction'])
            elif data['action'] == 'shoot':
                game.shoot(data['player'])

            # Update bullets after input
            game.update_bullets()

            # Send back current game state
            conn.send(pickle.dumps(game))

        except Exception as e:
            print("Client error:", e)
            break

    conn.close()

handle_client(conn)
