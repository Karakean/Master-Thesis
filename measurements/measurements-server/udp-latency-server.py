import socket

HOST = '0.0.0.0'
PORT = 2138
BUFFER_SIZE = 1024

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print(f"UDP server is running on port {PORT}...")

    while True:
        data, addr = server_socket.recvfrom(BUFFER_SIZE)
        if data:
            server_socket.sendto(data, addr)

if __name__ == "__main__":
    run_server()
