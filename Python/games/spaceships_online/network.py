import socket
import pickle

class Network:
    def __init__(self, server_ip="localhost", port=5555):
        # Create a TCP socket object for client-server communication
        # AF_INET indicates we're using IPv4
        # SOCK_STREAM indicates we're using TCP (reliable, ordered data stream)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Server IP address to connect to (default is localhost/127.0.0.1)
        self.server = server_ip
        
        # Port number to connect to on the server (default is 5555)
        self.port = port
        
        # Create a tuple of (IP, port) which is the format socket functions expect
        self.addr = (self.server, self.port)
        
        # Connect to the server and get the player ID (0 for yellow, 1 for red)
        # This happens immediately when a Network object is created
        self.player_id = self.connect()

    def connect(self):
        try:
            # Attempt to establish a connection to the server
            self.client.connect(self.addr)
            
            # After connecting, the server immediately sends the player ID
            # recv(2048) reads up to 2048 bytes of data from the server
            # pickle.loads() deserializes the data back into a Python object (in this case, an integer)
            return pickle.loads(self.client.recv(2048))
        except:
            # If connection fails, the function returns None implicitly
            pass

    def send(self, data):
        try:
            # Serialize the data (convert Python object to byte stream) using pickle
            # This allows us to send complex data structures over the network
            self.client.send(pickle.dumps(data))
            
            # Wait for and receive the server's response (updated game state)
            # This is a blocking call - it waits until data is received
            # The received data is deserialized from bytes back to a Python object
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            # Print any socket errors that occur during sending/receiving
            print(e)