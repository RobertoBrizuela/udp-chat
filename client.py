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
            print(message.decode())
        except:
            pass
        
t = threading.Thread(target=receive)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ('localhost', 9999))

while True: 
    message = input()
    
    if not message.strip():
        print("Please enter a message.")
        continue
    
    if message == '!q':
        exit()
    else:
        ts = datetime.now().strftime("%H:%M:%S")
        payload = f"[{ts}] {name}: {message}"
        client.sendto(payload.encode(), ('localhost', 9999))