import base64
import json
import os
import logging
import socket
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from dotenv import load_dotenv


load_dotenv()
logging.basicConfig(filename="output.log", level=logging.INFO)


def send(socket: socket.socket, data: str) -> None:
    socket.sendall(data.encode('utf-8'))
    dest_ip, dest_port = socket.getpeername()
    logging.info(f"Sending data to {dest_ip} to port {dest_port}: {data}")


def aes_key_from_key_material(key_material) -> bytes:
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"AES-key-derivation",
        backend=default_backend(),
    )
    return hkdf.derive(key_material.encode())


def encrypt_aes_cbc(plaintext: bytes, key: bytes) -> str:
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(json.dumps(plaintext).encode()) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_bytes = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_bytes).decode('utf-8')


def decrypt_aes_cbc(ciphertext_with_iv_base64: bytes, key: bytes) -> str:
    ciphertext_with_iv = base64.b64decode(ciphertext_with_iv_base64)
    iv, ciphertext = ciphertext_with_iv[:16], ciphertext_with_iv[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext_bytes.decode('utf-8')
