import socket
import time
import statistics

HOST = "127.0.0.1"
PORT = 2135
TIMEOUT = 10
TRIALS = 50

def run_client():
    time_pairs = {}  # key: send_time (float), value: recv_time or None

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(TIMEOUT)
        client_socket.connect((HOST, PORT))
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    for _ in range(TRIALS):
        send_time = time.time()
        send_bytes = str(send_time).encode()
        time_pairs[send_time] = None

        try:
            client_socket.sendall(send_bytes)

            data = client_socket.recv(1024)
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
        except Exception as e:
            print(f"Communication error: {e}")

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
