import socket
import time

HOST = 'mmfoqrnji6fbnn9p34ety7rw78xua5ewk1fgzscjq4uqxzw351sy.loki'
PORT = 2138
BUFFER_SIZE = 1024
DURATION = 10
MAX_SENT = 20 * 1024 * 1024 * DURATION # we do not expect more than 20MB/s so it makes no sense to send more 

def run_udp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        payload = b'e' * BUFFER_SIZE
        end_time = time.time() + DURATION
        total_sent = 0

        while time.time() < end_time and total_sent < MAX_SENT:
            s.sendto(payload, (HOST, PORT))
            total_sent += len(payload)

        s.sendto(b'__end__', (HOST, PORT))
        print(f"Sent {total_sent} bytes in {DURATION} seconds")

if __name__ == "__main__":
    run_udp_client()