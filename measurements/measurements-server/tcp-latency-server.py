import socket

HOST = '0.0.0.0'
PORT = 2135
BUFFER_SIZE = 1024

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"TCP server is running on port {PORT}...")

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"Connection from {client_addr}")

        try:
            while True:
                data = client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                client_socket.sendall(data)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()
            print(f"Connection with {client_addr} closed")

if __name__ == "__main__":
    run_server()
