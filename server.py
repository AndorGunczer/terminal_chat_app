import socket
import threading

def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 3201))
    server_socket.listen(5)
    print("Server listening on port 3200...")
    return server_socket

def handle_client(client_socket, client_address, server_socket):
    print(f"New connection from {client_address}")
    
    # reassure client about successful connection
    client_socket.send(f"Server at {server_socket.getsockname()[0]}: Connected to server".encode())
    
    while True:
        try:
            received = client_socket.recv(1024)
            if not received:
                print(f"Connection closed by {client_address}.")
                break
            print(f"Received from {client_address}: {received.decode()}")
        except Exception as e:
            print(f"Error receiving data from {client_address}: {e}")
            break
    
    client_socket.close()

def run_server():
    server_socket = create_server()
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, server_socket))
        client_thread.start()

run_server()