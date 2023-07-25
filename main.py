import sys
import os

from hillcipher import encrypt, decrypt
from argshandler import validate_args

encryption_ext = ".hc"

def encrypt_textfile(filepath, key):
    input_file = open(filepath, "r") # currently cannot encrypt binary files
    output_file = open(filepath + encryption_ext, "w")
    try:
        print(f"[*] Encrypting {input_file.name} ...")
        for line in input_file:
            enc_line = encrypt(line, key)
            output_file.write((enc_line.encode("utf-7")).decode("utf-8")+"\n")

        print("[*] Done.")

    except Exception as ex:
        print(f"Error: Encrypting {filepath}")

        output_file.close()
        os.remove(filepath + encryption_ext) # undo operation

    finally:
        input_file.close()

        if not output_file.closed:
            output_file.close()

        

def prompt(config):
    key = config["key"]
    while True:
        message = input("(Max 5100 chars) Ctrl-C to exit \n<message> : ")[:5100] # max 255 chars input
        
        # run encrypt/decrypt mode
        if config["mode"] == "encrypt":
            ciphertext = encrypt(message, key) # encrypt message (expecting plaintext)
            print(f"\nCiphertext:\t{ciphertext}\n") 

        else:
            plaintext = decrypt(message, key) # decrypt message (expecting ciphertext)
            print(f"\nPlaintext:\t{plaintext}\n")
        
def main():
    config = validate_args(sys.argv)

    try:
        # run encryption/decryption interactively (prompt) if no input/output 
        # filename specified
        if not config["filepath"]:
            prompt(config)

        else: #  encrypt/decrypt specified file
            if config["mode"] == "encrypt":
                encrypt_textfile(config["filepath"], config["key"])

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()