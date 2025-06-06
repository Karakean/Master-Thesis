import socket
import time

HOST = '0.0.0.0'
PORT = 2136
BUFFER_SIZE = 65535
TIMEOUT = 10

def run_udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"TCP throughput server is running on port {PORT}...")

    total_bytes = 0
    start_time = None
    last_packet_time = None

    client_socket, client_addr = server_socket.accept()
    print(f"Connection from {client_addr}")
    try:
        while True:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            now = time.time()
            if start_time is None:
                start_time = now
            last_packet_time = now
            total_bytes += len(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {client_addr} closed")

    if start_time is None:
        print("No data received.")
    else:
        duration = last_packet_time - start_time
        throughput_Kbps = (total_bytes * 8) / (duration * 1000)
        print(f"Received {total_bytes} bytes in {duration:.2f} seconds")
        print(f"Throughput: {throughput_Kbps:.3f} Kbps")

if __name__ == "__main__":
    run_udp_server()