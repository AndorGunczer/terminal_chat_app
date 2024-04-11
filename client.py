import socket
import threading

def create_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect(('127.0.0.1', 3206))

    return client_socket

def sending_function(server_socket):
    while True:
        text = input("Andor: ")

        server_socket.send(text.encode())
    return

def receiving_function(server_socket):
    while True:
        text = server_socket.recv(1024).decode()

        print(text)
    return

def run():
    server_socket = create_client()

    receiving_thread = threading.Thread(target=receiving_function, args=(server_socket,))
    sending_thread = threading.Thread(target=sending_function, args=(server_socket,))

    try: 
        receiving_thread.start()
        sending_thread.start()

        # receiving_thread.join()
        sending_thread.join()
    except Exception as e:
        print("threads error")
        server_socket.close()



run()