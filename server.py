import http.server
import socket

# def run(server_class = http.server.HTTPServer, handler_class = http.server.BaseHTTPRequestHandler) :
#     server_address = ('127.0.0.1', 3000)
#     httpd = server_class(server_address, handler_class)
#     httpd.serve_forever()

def create_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server_socket.bind(('127.0.0.1', 3205))

    server_socket.listen(5)
    return server_socket

def handle_client(client_socket):
    while True:
        try:
            received = client_socket.recv(1024)
            if len(received) == 0:  # Check if the message is empty
                break
            print("Received:", received.decode())
        
        except ConnectionResetError:
            print("Client closed the connection.")
            break

        except Exception as e:
            print(e)
            break
    client_socket.close()


def run():
    server_socket = create_socket()
    # Server is Listening

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"New connection from {client_address}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
            # client_thread.join()
        except Exception as e:
            server_socket.close()

run()