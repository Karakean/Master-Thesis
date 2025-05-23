import socket
import time
import statistics

HOST = "mmfoqrnji6fbnn9p34ety7rw78xua5ewk1fgzscjq4uqxzw351sy.loki"
PORT = 2136
TIMEOUT = 10
TRIALS = 50

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(TIMEOUT)

    time_pairs = {}  # key: send_time (float), value: recv_time or None

    for _ in range(TRIALS):
        send_time = time.time()
        send_bytes = str(send_time).encode()
        time_pairs[send_time] = None

        try:
            client_socket.sendto(send_bytes, (HOST, PORT))
            data, _ = client_socket.recvfrom(1024)
            recv_time = time.time()

            try:
                echoed_send_time = float(data.decode())
            except ValueError:
                print("Received malformed response.")
                continue

            if echoed_send_time in time_pairs and time_pairs[echoed_send_time] is None:
                time_pairs[echoed_send_time] = recv_time
                rtt = recv_time - echoed_send_time
                print(f"RTT = {rtt:.6f} sec")
            else:
                print("Mismatched or duplicate response.")

        except socket.timeout:
            print("Timeout occurred.")

        time.sleep(1)

    client_socket.close()

    # Results
    rtts = [
        recv - sent
        for sent, recv in time_pairs.items()
        if recv is not None
    ]

    avg_latency = sum(rtts) / len(rtts) if rtts else 0
    jitter = statistics.stdev(rtts) if len(rtts) > 1 else 0
    packet_loss = ((TRIALS - len(rtts)) / TRIALS) * 100

    print("\n--- Results ---")
    print(f"Average Latency: {avg_latency * 1000:.2f} ms")
    print(f"Jitter: {jitter * 1000:.2f} ms")
    print(f"Packet Loss: {packet_loss:.2f}%")

if __name__ == "__main__":
    run_client()
