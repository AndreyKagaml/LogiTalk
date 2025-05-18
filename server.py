import socket
import threading

HOST = '127.0.0.1'
PORT = 22

clients = []

def broadcast(data, exclude_socket=None):
    for client in clients:
        if client != exclude_socket:
            try:
                client.sendall(data)
            except:
                pass

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            broadcast(data, exclude_socket=client_socket)
        except:
            break
    if client_socket in clients:
        clients.remove(client_socket)
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(15)
    print(f"Server has started {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address} connected")
        clients.append(client_socket)

        t = threading.Thread(target=handle_client, args=(client_socket,))
        t.start()

main()