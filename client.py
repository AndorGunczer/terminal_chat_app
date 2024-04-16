import tkinter as tk
from tkinter import messagebox
import socket
import threading

class myGui:
    def __init__(self):
        self.root = tk.Tk()

        self.root.geometry("600x700")
        self.label = tk.Label(self.root, text="AndorChat Client")
        self.label.pack()

        self.messengerWin = tk.Text(self.root, height=30, width=38)
        self.messengerWin.pack()
        
        frame = tk.Frame(self.root)
        frame.pack()

        self.serverConnect = tk.Text(frame, height=2, width=14)
        self.serverConnect.pack(side="left")
        
        self.portConnect = tk.Text(frame, height=2, width=14)
        self.portConnect.pack(side="left")

        # Button for connecting to the server
        self.buttonConnect = tk.Button(frame, text="Connect", command=self.connect_to_server)
        self.buttonConnect.pack(side="left")

        self.userText = tk.Text(self.root, height=2, width=38)
        self.userText.pack()

        # Button for sending messages
        self.userTextButton = tk.Button(self.root, text="Send", command=self.send_message)
        self.userTextButton.pack()

        self.root.bind('<Return>', self.send_message)

        self.root.mainloop()

    def connect_to_server(self):
        ipaddr = self.serverConnect.get("1.0", "end-1c")  # Get the IP address from the text widget
        port = int(self.portConnect.get("1.0", "end-1c"))  # Get the port from the text widget

        # Call the create_client method of the Client class
        self.client = Client(self)
        self.client.create_client(ipaddr, port)
        self.client.run_client(self)

    def send_message(self, event = None):
        message = self.userText.get("1.0", "end-1c").strip()  # Get the message from the text widget
        if message == "":
            return
        self.userText.delete('1.0', tk.END)
        if self.client:
            self.client.send_message(message)
        else:
            messagebox.showerror("Error", "You need to connect to the server first")

class PopupWindow:
    #not sure if the structure is fine
    def __init__(self, parent, client):
        self.parent = parent
        self.popup = tk.Toplevel(parent.root)
        print(1)

        self.popup.geometry("600x700")
        print(2)

        self.label = tk.Label(self.popup, text="Choose a nickname:").pack()
        print(3)
        self.nicknameText = tk.Text(self.popup, height=1, width=60)
        self.nicknameText.pack()
        print(4)
        self.nicknameButton = tk.Button(self.popup, height=1, width=60, text="Submit", command=lambda: self.submit(client))
        print(5)
        self.nicknameButton.pack()

        # Store the PopupWindow instance in the parent
        # parent.popup_window = self
        # self.popup.mainloop()

    def submit(self, client):
        text = self.nicknameText.get("1.0", "end-1c").strip()
        self.send_message(client, text)
        self.popup.destroy()  # Destroy the popup window

    def send_message(self, client, text):
        message = text  # Get the message from the text widget
        if message == "":
            return
        self.nicknameText.delete('1.0', tk.END)
        if client:
            client.client_socket.send(message.encode())
        else:
            messagebox.showerror("Error", "You need to connect to the server first")
        

class Client:
    def __init__(self, gui):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nickname = ""
        self.gui = gui

    def create_client(self, ipaddr, port):
        try:
            self.client_socket.connect((ipaddr, port))
            answer = self.client_socket.recv(1024).decode()
            if answer:
                print(answer)
                self.client_socket.send("ACK: Connection".encode())
                # Set Nickname
                popup = PopupWindow(self.gui, self)
                print("Went further")
                # self.nickname = input("Enter your nickname: ")
                # self.client_socket.send(self.nickname.encode())
                #self.client_socket.
            else:
                print("Failed to connect to server")
        except Exception as e:
            print("Connection error:", e)

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode())
        except Exception as e:
            print("Sending message error:", e)

    def receiving_function(self, gui):
        while True:
            try:
                text = self.client_socket.recv(1024).decode()
                if not text:
                    print("Server disconnected.")
                    break
                print(text + "\n")
                gui.messengerWin.insert(tk.END, text + "\n")
                gui.messengerWin.see(tk.END)
            except Exception as e:
                print("Receiving message error:", e)
                break

    def run_client(self, gui):
        receiving_thread = threading.Thread(target=self.receiving_function, args=(gui,))
        receiving_thread.start()

if __name__ == "__main__":
    gui = myGui()