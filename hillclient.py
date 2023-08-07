import socket
import threading

from hillcipher import encrypt, decrypt

def connect_to_svr(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4 tcp socket
    try:
        return sock.connect((address, port))
    
    except InterruptedError as interruptErr:
        print(f"Error: Connection to {address}:{port} was interrupted.")

    except TimeoutError as timeoutErr:
        print("Error: Connection timed out.")

    except Exception as ex:
        print(f"Error: Unexpected error {ex}.")

    return None

def recv_messages(sock):

    # Continuously wait for messages
    while True:
        try:
            message : bytes = sock.recv(1024)
            print(f"=> {message.decode(encoding='ascii', errors='replace')}")

        except InterruptedError as interruptErr:
            print("Error: Receiver interrupted. Moving on...")
        

def send_message(sock, message : str):
    try:
        msg_bytes = bytes(message, "ascii")
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
        while True:
            message = input("<enter message> (Ctrl-C to exit): ")
            
            send_message( sock, encrypt(f"[{uname}] "+ message) )

    except InterruptedError:
        exit()

    except Exception as ex:
        print(f"Error: Unexpected error {ex}.")
        exit()

def terminate():
    print("Bye bye!")
    exit()

def main():
    
    sock = connect_to_svr("192.168.56.1", 890)
    
    if not sock:
        print("Connection failed. Aborting!")
        terminate()

    receiver_thread = threading.Thread(target=recv_messages, args=(sock))
    receiver_thread.start() # have separate thread to constantly receive messages
    prompt("CommanderX", "L0v3IsK3y", sock)


if __name__=="__main__":
    main()