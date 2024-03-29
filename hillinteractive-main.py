import sys
import os

from lib.hillcipher import encrypt, decrypt
from lib.argshandler import validate_args


def prompt(config):
    key = config["key"]
    while True:
        message = input("(Max 5100 chars) Ctrl-C to exit \n<message> : ")[:5100]  # max 255 chars input

        # run encrypt/decrypt mode
        if config["mode"] == "encrypt":
            ciphertext = encrypt(message, key)  # encrypt message (expecting plaintext)
            print("\nCiphertext:\t", ciphertext, "\n")

        else:
            plaintext = decrypt(message, key)  # decrypt message (expecting ciphertext)
            print("\nPlaintext:\t", plaintext, "\n")


def main():
    config = validate_args(sys.argv)

    try:
        # run encryption/decryption interactively (prompt) if no input/output 
        prompt(config)

    except KeyboardInterrupt:
        pass

    print("\nBye bye!")


if __name__ == "__main__":
    main()
