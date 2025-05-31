import json
import logging
import os
import random
import socket
import time
from utils import send, aes_key_from_key_material, decrypt_aes_cbc

BUFFER_SIZE = 1024
HOST = "0.0.0.0"
PORT = os.environ['PORT']
KEY_MATERIAL = os.environ['KEY_MATERIAL'] # usually this is negotiated, for example, via a Diffie-Hellman exchange
ROUTER_MODE = os.environ['ROUTER_MODE']
MIX_NODE_THRESHOLD = os.environ['MIX_NODE_THRESHOLD']
NEXT_NODE_HOSTNAME = os.environ.get('NEXT_NODE_HOSTNAME', "")
NEXT_NODE_PORT = int(os.environ.get('NEXT_NODE_PORT', "-1"))


def release_mix_buffer(socket: socket.socket, messages_buffer: list) -> None:
    logging.info("Mix node threshold reached, sending buffered messages.")
    for msg in messages_buffer:
        time.sleep(random.random() + 1) # Additional delay
        send(socket, msg)
    messages_buffer.clear()


def handle_mix_message(socket: socket.socket, messages_buffer: list, data: str) -> None:
    messages_buffer.append(data)
    logging.info(f"Message buffered. Current count: {len(messages_buffer)}")
    random.shuffle(messages_buffer) # Mixing
    if len(messages_buffer) == int(MIX_NODE_THRESHOLD):
        release_mix_buffer(socket, messages_buffer)


def handle_message(socket: socket.socket, content: str, messages_buffer: list) -> None:
    data_json = json.loads(content)
    if data_json.get("forward_to") is None:
        return
    data = data_json["data"]
    if ROUTER_MODE == "ONION-ROUTING":
        send(socket, data)
    else:
        handle_mix_message(socket, messages_buffer, data)


def create_listening_socket() -> socket.socket:
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.bind((HOST, int(PORT)))
    listening_socket.listen(5)
    logging.info(f"Listening on port {PORT}...")
    return listening_socket


def create_sending_socket():
    sending_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if NEXT_NODE_HOSTNAME and NEXT_NODE_PORT != -1:
        sending_socket.connect((NEXT_NODE_HOSTNAME, NEXT_NODE_PORT))
        logging.info(f"Connected to next node at {NEXT_NODE_HOSTNAME}:{NEXT_NODE_PORT}")
    return sending_socket


def handle_incoming_communication(key: bytes, messages_buffer: list, sending_socket: socket.socket, client_socket: socket.socket, client_ip: str) -> None:
    while True:
        received_data = client_socket.recv(BUFFER_SIZE)
        if not received_data:
            break
        logging.getLogger().info("\n")
        logging.info(f"Received message from {client_ip} on port: {PORT}.\n" + 
                     f"Content before decryption: {received_data}")
        decrypted_message = decrypt_aes_cbc(received_data, key)
        logging.info(f"Conent after decryption: {decrypted_message}")
        handle_message(sending_socket, decrypted_message, messages_buffer)


def disconnect(sending_socket, client_socket):
    client_socket.close()
    sending_socket.close()
    logging.info("Connection closed.")


def run_server() -> None:
    key = aes_key_from_key_material(KEY_MATERIAL)
    messages_buffer = []
    listening_socket = create_listening_socket()
    sending_socket = create_sending_socket()
    while True:
        client_socket, client_addr = listening_socket.accept()
        try:
            handle_incoming_communication(key, messages_buffer, sending_socket, client_socket, client_addr[0])
        except Exception as e:
            logging.error(f"Error: {e}")
        finally:
            disconnect(sending_socket, client_socket)


def main():
    run_server()


if __name__ == "__main__":
    main()
