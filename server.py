import socket
import threading


host = socket.gethostname()
port = 49153


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen()

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s2.bind((host, 60001))
s2.listen()

clients = []
nicknames = []

fclients = []
fnicknames = []

def broadcast(massage):
    for client in clients:
        client.send(massage)

def handle(client):
    while True:
        try:

            # now = datetime.now().time().strftime("%H:%M:%S")  # time object
            # date = datetime.now().strftime("%Y-%m-%d")  # date object
            massage = client.recv(1024)
            # massage = f'[{date}] {now}: {massage}'
            broadcast(massage)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def recieve():
    while True:
        client, address = s.accept()
        print(F"Connected with {address}, {client}")
        # client.send("NICKNAME?".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        print(f'{client} + {nickname} + {address}')
        broadcast(f"{nickname} connected with server \n".encode('utf-8'))
        # client.send("connected to server".encode('utf-8'))
        clients.append(client)
        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

print("server is running")
recieve()