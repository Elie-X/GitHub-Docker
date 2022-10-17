import socket, tqdm, os
SERVER_HOST = socket.gethostname()
SERVER_PORT = 1234
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))

while True:
    s.listen()
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    client_socket, address = s.accept()
    print(f"[+] {address} is connected.")


    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)

    filename = os.path.basename(filename)
    filesize = int(filesize)

    print(f"[*] Commencing upload of {filename}")
    progress = tqdm.tqdm(range(filesize), f"Received {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    remaining_buffer = filesize
    with open(filename, "wb") as f:
        while True:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:
                print(f"File transfer {filename} over.")
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
print(f"[*] Closing server.")
client_socket.close()
s.close()

