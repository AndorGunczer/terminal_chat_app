import socket
import threading

class Server:

    def __init__(self):
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ipaddr = input("Server IP: ")
        self.port = int(input("Port: "))

    def broadcast(self, client_socket, received):
        for client in self.clients:
            # if client != client_socket:
            client.send(f"{self.clients[client_socket]}: {received}".encode())

    def activate_socket(self):
        self.server_socket.bind((self.ipaddr, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on port {self.port}...")
        return self.server_socket

    def handle_client(self, client_socket, client_address):
        print(f"New connection from {client_address}")
        
        # reassure client about successful connection
        client_socket.send(f"Server at {self.server_socket.getsockname()[0]}: Connected to server".encode())
        client_socket.recv(1024).decode() == "ACK: Connection"
        
        nicknameInput = client_socket.recv(1024).decode()

        self.clients[client_socket] = nicknameInput
        
        while True:
            try:
                received = client_socket.recv(1024).decode()
                if not received:
                    print(f"Connection closed by {client_address}.")
                    break
                # print(f"Received from {client_address}: {received.decode()}")
                self.broadcast(client_socket, received)
            except Exception as e:
                print(f"Error receiving data from {client_address}: {e}")
                break
        
        client_socket.close()

    def run_server(self):
        self.activate_socket()

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

def run():
    server1 = Server()
    server1.run_server()

run()