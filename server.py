import socket
import threading
import queue
from datetime import datetime

messages = queue.Queue()
users = {}  # { (ip,port): name }

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 9999))

def receive():
    while True:
        try:
            msg, addr = server.recvfrom(1024)
            print(f"[RECEIVED from {addr}] {msg.decode()}")
            messages.put((msg, addr))
        except Exception as e:
            print(f"Error receiving: {e}")

def broadcast():
    while True:
        try:
            message, addr = messages.get()
            text = message.decode().strip()

            if text.startswith("SIGNUP_TAG:"):
                name = text.split(":", 1)[1]
                users[addr] = name
                notice = f"✅ {name} has joined the chat."
                print(f"[Server] {notice}")
                for client_addr in users:
                    server.sendto(notice.encode(), client_addr)

            elif text == "LIST_USERS_TAG":
                lista = ", ".join(users.values())
                reply = f"Online users: {lista}"
                server.sendto(reply.encode(), addr)

            elif text == "DISCONNECT_TAG":
                if addr in users:
                    name = users.pop(addr)
                    notice = f"❌ {name} has been disconnected."
                    print(f"[Server] {notice}")
                    for client_addr in users:
                        server.sendto(notice.encode(), client_addr)

            else:
                if addr not in users:
                    continue
                sender = users[addr]
                ts = datetime.now().strftime("%H:%M:%S")
                msg = f"[{ts}] {sender}: {text}"
                print(f"[Server] {msg}")
                for client_addr in list(users):
                    try:
                        server.sendto(msg.encode(), client_addr)
                    except:
                        users.pop(client_addr, None)

        except Exception as e:
            print(f"Broadcast error: {e}")




t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)
t1.start()
t2.start()

print("✅ UDP server running on port 9999")
t1.join()
t2.join()

