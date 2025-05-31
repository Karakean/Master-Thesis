import os
import socket

from utils import send, aes_key_from_key_material, encrypt_aes_cbc


SINGLE_HOP_PROXY_PORT = int(os.environ['SINGLE_HOP_PROXY_PORT'])
ENTRY_NODE_PORT = int(os.environ['ENTRY_NODE_PORT'])
SINGLE_HOP_PROXY_KEY_MATERIAL = os.environ['SINGLE_HOP_PROXY_KEY_MATERIAL']
ENTRY_NODE_KEY_MATERIAL = os.environ['ENTRY_NODE_KEY_MATERIAL']
MIDDLE_NODE_KEY_MATERIAL = os.environ['MIDDLE_NODE_KEY_MATERIAL']
EXIT_NODE_KEY_MATERIAL = os.environ['EXIT_NODE_KEY_MATERIAL']


def send_to_single_hop_proxy(socket: socket.socket, message: bytes) -> None:
    single_hop_proxy_key = aes_key_from_key_material(SINGLE_HOP_PROXY_KEY_MATERIAL)
    encrypted_message = encrypt_aes_cbc(message, single_hop_proxy_key)
    send(socket, encrypted_message)
    print("Data successfully sent to the single hop proxy.")


def send_layered(socket: socket.socket, message: str) -> None:
    exit_key = aes_key_from_key_material(EXIT_NODE_KEY_MATERIAL)
    encrypted_message_exit = encrypt_aes_cbc(message, exit_key)

    middle_key = aes_key_from_key_material(MIDDLE_NODE_KEY_MATERIAL)
    data_for_middle_node = {"forward_to": "exit-node", "data": encrypted_message_exit}
    encrypted_message_middle = encrypt_aes_cbc(data_for_middle_node, middle_key)

    entry_key = aes_key_from_key_material(ENTRY_NODE_KEY_MATERIAL)
    data_for_entry_node = {"forward_to": "middle-node", "data": encrypted_message_middle}
    encrypted_message_entry = encrypt_aes_cbc(data_for_entry_node, entry_key)
    send(socket, encrypted_message_entry)
    print("Data successfully sent to the first node of the anonymous communication network.")


def create_socket(port: int) -> socket.socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    return client_socket


def handle_message(mode_name: str, client_socket: socket.socket, input_message: str) -> None:
    request = {
        "website": "http://very-sensitive-website.com",
        "data": input_message  # This data may be encrypted with TLS if using HTTPS or unencrypted if using HTTP
    }
    if mode_name == 'anonymous communication network':
        send_layered(client_socket, request)
    else:
        send_to_single_hop_proxy(client_socket, request)


def handle_mode(mode_name: str, port: int) -> None:
    client_socket = create_socket(port)
    while True:
        input_data = input(f"Enter message to send through the {mode_name} or type 'exit' to quit: ")
        if not input_data:
            print("No message entered. Please enter message to send or type 'exit' to quit.")
            continue
        elif input_data.lower() == 'exit':
            break
        handle_message(mode_name, client_socket, input_data)
    client_socket.close()


def run_client() -> None:
    print("Select mode:\n1. Single hop proxy\n2. Anonymous communication network")
    mode = input("Enter 1 or 2: ").strip()
    if mode == '1':
        handle_mode('single hop proxy', SINGLE_HOP_PROXY_PORT)
    elif mode == '2':
        handle_mode('anonymous communication network', ENTRY_NODE_PORT)
    else:
        raise ValueError("Invalid mode. Please enter 1 to use single hop proxy or 2 for anonymous communication network.")


def main():
    run_client()


if __name__ == "__main__":
    main()
