import socket
import threading
import sys

from hillcipher import encrypt, decrypt

prompt_text : str = "<You>: "

def usage():
    print("Usage:\n\t")
    print("program.py -uname <user_name> -key <encryption_key> -host <svr_address> -port <port>")
    exit()

def safe_read_arg(option, program_args):
    if not option in program_args: # option must be valid
        print(f"Not all mandatory options were provided.\n")
        usage()

    arg_index = program_args.index(option) + 1 # must not be null
    if arg_index >= len(program_args):
        print(f"Argument for option {option} not found.")
        usage()

    arg = program_args[arg_index]
    if arg in ("-uname", "-key", "-host", "-port"): # argument must not be an option
        print(f"Invalid argument {arg}. Cannot be an option.")
        usage()

    return arg

def connect_to_svr(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4 tcp socket
    try:
        sock.connect((address, port))
        return sock

    except InterruptedError as interruptErr:
        print(f"Error: Connection to {address}:{port} was interrupted.")

    except TimeoutError as timeoutErr:
        print("Error: Connection timed out.")

    except Exception as ex:
        print(f"Error: Unexpected error {ex}.")

    return None

def recv_messages(sock, key):

    # Continuously wait for messages
    while True:
        try:
            message : bytes = sock.recv(1024)
            decoded_msg = message.decode(encoding='utf-8', errors='replace')

            print(f"\r{' '*len(prompt_text)}\n{decrypt(decoded_msg, key)}\n") # overwrite current prompt before output new message
            print(prompt_text, end="", flush=True)

        except InterruptedError as interruptErr:
            print("Error: Receiver interrupted. Moving on...")
        

def send_message(sock, message : str):
    try:
        msg_bytes = bytes(message, "utf-8")
        bytes_sent = sock.send(msg_bytes)

        # send remaining bytes if not all sent
        while bytes_sent < len(msg_bytes):
            bytes_sent += sock.send(msg_bytes[bytes_sent:]) 

        print(f"Sent: {bytes_sent} bytes.")

    except Exception as ex:
        print(f"Error: Sending message {message}")
        print(ex)
    

def prompt(uname, key, sock):
    print("Welcome to HushCat!")
    try:
        print(prompt_text, end="", flush=True)
        while True:
            message = input()
            
            send_message( sock, encrypt(f"<{uname}>: "+ message, key) )
            print(prompt_text, end="", flush=True)

    except InterruptedError:
        exit()

    except KeyboardInterrupt:
        exit()

    except Exception as ex:
        print(f"Error: Unexpected error {ex}.")
        exit()

def terminate():
    print("Bye bye!")
    exit()

def main():
    
    uname = safe_read_arg("-uname", sys.argv)
    key = safe_read_arg("-key", sys.argv)
    host = safe_read_arg("-host", sys.argv)
    port = int(safe_read_arg("-port", sys.argv))

    sock = connect_to_svr(host, port)
    
    if not sock:
        print("Connection failed. Aborting!")
        terminate()

    receiver_thread = threading.Thread(target=recv_messages, args=(sock, key))
    receiver_thread.start() # have separate thread to constantly receive messages
    prompt(uname, key, sock)


if __name__=="__main__":
    main()

#TODO: Upon connection send client ID hash to server for authentication
#TODO: Add client ID to key as salt, to form new encryption key