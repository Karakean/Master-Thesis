import socket
import time

HOST = '0.0.0.0'
PORT = 2138
BUFFER_SIZE = 65535
TIMEOUT = 10

def run_udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        s.settimeout(TIMEOUT)
        print(f"UDP throughput server listening on {HOST}:{PORT}")

        total_bytes = 0
        start_time = None
        last_packet_time = None

        while True:
            try:
                data, addr = s.recvfrom(BUFFER_SIZE)
                now = time.time()
                if start_time is None:
                    start_time = now
                last_packet_time = now
                total_bytes += len(data)
            except socket.timeout:
                break

        if start_time is None:
            print("No data received.")
        else:
            duration = last_packet_time - start_time
            throughput_Kbps = (total_bytes * 8) / (duration * 1000)
            print(f"Received {total_bytes} bytes in {duration:.2f} seconds")
            print(f"Throughput: {throughput_Kbps:.3f} Kbps")

if __name__ == "__main__":
    run_udp_server()