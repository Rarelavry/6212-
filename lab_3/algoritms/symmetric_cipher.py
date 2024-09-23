"""
This module implements functionality (key generation, encryption and decryption) 
for symmetric encryption
"""

import os

from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

from constants import (
    PKCS7_BLOCK_SIZE,
)
from serialization import Serialization
from functional import Functional


class Symmetric:
    """
    This class provides the definition of key generation functions for
    symmetric encryption, as well as encryption and decryption using it
    """

    def __init__(self):
        pass

    def generate_key(bytes_num: int) -> bytes:
        """generate symmetric key

        Args:
            bytes_num (int):key_len

        Returns:
            bytes: symmetric key
        """
        return os.urandom(bytes_num)

    def encrypt(
        text_file_path: str,
        path_to_symmetric: str,
        encrypted_text_file_path: str,
        ) -> bytes:
        """encryption by symmetric key (SEED)

        Args:
            text_file_path (str) : path to origin text
            path_to_symmetric (str) : path to symmetric key
            encrypted_text_file_path (str) : file path for encrypted text

        Returns:
            str: encrypted text
        """
        # Чтение исходного текста и симметричного ключа
        origin_text = Functional.read_file(text_file_path)
        symmetric_key = Serialization.deserialize_symmetric_key(path_to_symmetric)

        if len(symmetric_key) != 16:  # Проверка длины ключа (128 бит)
            raise ValueError("Ключ должен быть длиной 16 байт (128 бит)")

        # Инициализация шифра SEED в режиме ECB
        cipher = Cipher(
            algorithms.SEED(symmetric_key),
            mode=modes.ECB(),  # ECB режим
            backend=default_backend()
        )

        # Дополнение текста до кратного 16 байтам (PKCS7)
        padder = padding.PKCS7(PKCS7_BLOCK_SIZE).padder()
        text_to_bytes = bytes(origin_text, "UTF-8")
        padded_text = padder.update(text_to_bytes) + padder.finalize()

        # Инициализация шифратора
        encryptor = cipher.encryptor()

        # Шифрование текста
        encrypted_text = encryptor.update(padded_text) + encryptor.finalize()

        # Сохранение зашифрованного текста в файл
        Functional.write_file_bytes(encrypted_text_file_path, encrypted_text)

        return encrypted_text


    def decrypt(
            path_to_symmetric: str,
            path_to_encrypted_text: str,
            path_to_decrypted_text: str,
        ) -> str:
        """decryption by symmetric key (SEED)

        Args:
            path_to_symmetric (str) : path to key
            path_to_encrypted_text (str) : path to encrypted file
            path_to_decrypted_text (str) : path to decrypted file

        Returns:
            str: decrypted text
        """
        # Чтение зашифрованного текста и симметричного ключа
        encrypted_text = Functional.read_file_bytes(path_to_encrypted_text)
        symmetric_key = Serialization.deserialize_symmetric_key(path_to_symmetric)

        if len(symmetric_key) != 16:  # Проверка длины ключа (128 бит)
            raise ValueError("Ключ должен быть длиной 16 байт (128 бит)")

        # Инициализация расшифровщика SEED в режиме ECB
        cipher = Cipher(
            algorithms.SEED(symmetric_key),
            mode=modes.ECB(),
            backend=default_backend()
        )

        # Инициализация расшифровщика
        decryptor = cipher.decryptor()

        # Расшифровка текста
        decrypted_text = decryptor.update(encrypted_text) + decryptor.finalize()

        # Удаление дополнений (unpadding)
        unpadder = padding.PKCS7(PKCS7_BLOCK_SIZE).unpadder()
        unpadded_dc_text = unpadder.update(decrypted_text) + unpadder.finalize()

        # Преобразование байтов обратно в строку
        dec_unpad_text = unpadded_dc_text.decode("UTF-8")

        # Сохранение расшифрованного текста в файл
        Functional.write_file(path_to_decrypted_text, dec_unpad_text)

        return dec_unpad_text
