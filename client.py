import socket
import threading
import random 
from datetime import datetime

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(('localhost', random.randint(8000, 9000)))

name = ""
while not name.strip():
    name = input("Enter your name or nickname: ").strip()
    if not name:
        print("Please enter your name.")

def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(f"\r{message.decode()}\nEnter your message: ", end='')
        except:
            pass
        
t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ('localhost', 9999))

while True:
    message = input("Enter your message: ")
    # check if the message is empty
    if not message.strip():
        print("⚠️  You cannot send an empty message.")
        continue

    # command to list users
    if message.strip() == '/list':
        client.sendto("LIST_USERS_TAG".encode(), ('localhost', 9999))
        continue

    if message == '!q':
        # send a disconnection notice to the server
        client.sendto("DISCONNECT_TAG".encode(), ('localhost', 9999))
        print("🚪 You have successfully left the chat.")
        break  # exit main loop

    # timestamp + normal message
    client.sendto(message.encode(), ('localhost', 9999))