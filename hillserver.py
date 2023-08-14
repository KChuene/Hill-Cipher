import socket
import sys
import threading

# prospect of future development
modules = ["secured", "plain"] 
options = ["-h", "-host", "-port", "-basekey", "-invites"]
make_secure = False


connections = []

def log_newconnection(host, socket):
    global connections

    client = {
        "host": host, # ipv4 address
        "user": None, # username
        "key": None,
        "socket": socket # socket
    }
    connections.append(client)

def usage():
    print("\nHushChat server for relaying encrypted communication.\n")
    print("Usage:\n\t program.py -host <bind_address> -port <bind_port>")
    exit()


def safe_read_args(option, argv):
    if not option in argv:
        print("Not all mandatory options were provided.")
        usage()


    arg_index = argv.index(option) + 1
    if arg_index >= len(argv):
        print(f"Argument expected for {option}. None found.")
        usage()

    arg = argv[arg_index]
    if arg in options:
        print(f"Argument {arg} cannot be an option.")
        usage()

    return arg


def send_message(sender, connection, data):
    bytes_sent = connection.send(data)

    while bytes_sent != len(data):
        bytes_sent += connection.send(data[bytes_sent:])

    print(f"sent to: {sender}")

def forward_message(data, sender_address):
    global connections

    for connection in connections:

        # skip forwarding message to original sender
        if connection["host"]==sender_address:
            continue

        send_thread = threading.Thread(target=send_message, args=(sender_address, connection["socket"], data))
        send_thread.start()


def recv_messages(conn_sock, address):
    # Key exchange / Id authentication

    try:
        while True:
            data = conn_sock.recv(1024)

            if len(data) > 0:
                print(f">>> forward {len(data)} bytes from {address}")
                forward_message(data, address)

    except KeyboardInterrupt as keyInterrupt:
        terminate()

    except Exception as ex:
        pass

    return None

def spawn_listener(host, port):
    global connections

    print(f"[*] binding socket to {host}:{port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ipv4 tcp socket
    sock.bind((host, port))
    
    conn_sock = None

    print("[*] listening for connections...")
    while True:
        sock.listen()
        conn_sock, address_info = sock.accept()
        print(f"--> Connection from {address_info[0]} port {address_info[1]}")

        # log client info and connection sock
        log_newconnection(address_info[0], conn_sock)

        recv_thread = threading.Thread(target=recv_messages, args=(conn_sock, address_info[0]))
        recv_thread.start()

def terminate():
    for connection in connections:
        connection["socket"].shutdown() # inform other end's socket of closure
        connection["socket"].close()

    print("Bye bye!")
    exit()

def main():
    if len(sys.argv) <= 1 or sys.argv[1] == "-h":
        usage()

    try:
        host = safe_read_args("-host", sys.argv)
        port = int(safe_read_args("-port", sys.argv))
        
        if host and port:
            spawn_listener(host, port)

    except KeyboardInterrupt as keyboardInt:
        terminate()

    except Exception as ex:
        print(f"Unexpected error: {ex}")
        terminate()



if __name__=="__main__":
    main()


#TODO: Upon connection received client ID hash, and validate ID against list of authorized ID hashes
#TODO: Use client ID as salt to form client key
#TODO: Decrypt received data using sender key, Forward data for each recipient encrypted with recipient key
#TODO: Improve exception handingling, especially against user input