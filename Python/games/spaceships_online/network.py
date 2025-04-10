# network.py

import socket
import pickle  # for object serialization

class Network:
    def __init__(self, host='localhost', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = host  # IP of the server
        self.port = port
        self.addr = (self.server, self.port)
        self.connect()

    def connect(self):
        """Connects to the server"""
        try:
            self.client.connect(self.addr)
        except Exception as e:
            print("Connection failed:", e)

    def send(self, data):
        """
        Sends Python object to the server and waits for a response.
        Returns the response from the server.
        """
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))  # Receive game state
        except Exception as e:
            print("Send failed:", e)
            return None

    def close(self):
        self.client.close()
