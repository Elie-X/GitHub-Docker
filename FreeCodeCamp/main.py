#!/usr/bin/env python3

import socket, tqdm, os
SERVER_HOST = socket.gethostname()
SERVER_PORT = 1234
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))

s.listen()
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

client_socket, address = s.accept()
print(f"[+] {address} is connected.")


print("Docker is magic!")

