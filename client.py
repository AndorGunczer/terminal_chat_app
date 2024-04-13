import socket
import threading

class Client:

    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ipaddr = input("Server IP: ")
        self.port = int(input("Server port: "))
        self.nickname = ""

    def create_client(self):
        # Connection Handshake

        self.client_socket.connect((self.ipaddr, self.port))
        answer = self.client_socket.recv(1024).decode()
        if (answer):
            print(answer)
            self.client_socket.send("ACK: Connection".encode())
        else:
            print(f"Failed to connect to server")
            return ''

        # Set Nickname
        print(self.client_socket.recv(1024).decode())
        self.nickname = input()
        self.client_socket.send(self.nickname.encode())

        return self.client_socket

    def sending_function(self, server_socket):
        while True:
            text = input("")

            server_socket.send(text.encode())
        return

    def receiving_function(self, server_socket):
        while True:
            text = server_socket.recv(1024).decode()

            print(text + "\n")
        return

    def run_client(self):
        server_socket = self.create_client()

        receiving_thread = threading.Thread(target=self.receiving_function, args=(server_socket,))
        sending_thread = threading.Thread(target=self.sending_function, args=(server_socket,))

        try: 
            receiving_thread.start()
            sending_thread.start()

            # receiving_thread.join()
            sending_thread.join()
        except Exception as e:
            print("threads error")
            server_socket.close()

def run():
    client1 = Client()
    client1.run_client()

run()