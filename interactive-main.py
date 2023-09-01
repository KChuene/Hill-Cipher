import sys
import os

from lib.hillcipher import encrypt, decrypt
from lib.argshandler import validate_args

encryption_ext = ".hc"
decryption_suffx = "decrypt"

def decrypt_binary(filepath, key):
    input_file = None
    output_file = None

    
    try:
        input_file = open(filepath, "rb")
        output_file = open(filepath + decryption_suffx, "wb")

        print(f"[*] Decrypting {input_file.name} (binary mode)...")
        for line in input_file:
            dec_result = decrypt(str(line), key) # decrypt requires string
            output_file.write(bytes(dec_result, "utf-8"))

    except Exception as ex:
        print(f"Error: Decryption {filepath}")
        raise ex
    
    finally:
        if input_file:
            input_file.close()

        if output_file:
            output_file.close()

def encrypt_textfile(filepath, key):

    input_file = None
    output_file = None

    try:
        input_file = open(filepath, "r")
        output_file = open(filepath + encryption_ext, "w")

        print(f"[*] Encrypting {input_file.name} (text mode)...")
        for line in input_file:

            enc_line = encrypt( line , key)
            output_file.write(str( enc_line.encode("utf-8") )) # write requires string

    except Exception as ex:
        print(f"Error: Encrypting {filepath}")
        raise ex

    finally:
        if input_file:
            input_file.close()

        if output_file:
            output_file.close()

def encrypt_binaryfile(filepath, key):

    input_file = None
    output_file = None

    try:
        input_file = open(filepath, "rb")
        output_file = open(filepath + encryption_ext, "wb")

        print(f"[*] Encrypting {input_file.name} (binary mode) ...")
        for line in input_file:

            enc_line = encrypt( str(line) , key) # encrypt requires strings
            output_file.write(bytes(enc_line, "utf-8")) # encoding requires bytes

    except Exception as ex:
        print(f"Error: Encrypting {filepath}")
        raise ex

    finally:
        if input_file:
            input_file.close()

        if output_file:
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

        elif config["mode"] == "encrypt": #  encrypt/decrypt specified file

            if config["isbinary"]:
                encrypt_binaryfile(config["filepath"], config["key"])
            
            else:
                encrypt_textfile(config["filepath"], config["key"])

        else:
            decrypt_binary(config["filepath"], config["key"])

        print("[*] Done.")

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()