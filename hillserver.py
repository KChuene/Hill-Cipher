import socket
from optparse import OptionParser
import threading

modules = ["secured", "plain"]
options = ["-h", "-host", "-port", "-basekey", "-invites"]
make_secure = False

client = {
    "host": None, # ipv4 address
    "user": None, # username
    "key": None,
    "socket": None # socket
}
connections = []

def parse_args():
    optparser = OptionParser()
    optparser.add_option("-h", help="Show this information.")
    optparser.add_option("-host", help="The IPv4 address to bind to.")
    optparser.add_option("-port", help="The local port to bind to.")

    return optparser.parse_args()

def send_message(connection, data):
    bytes_sent = connection.send(data)

    while bytes_sent != len(data):
        bytes_sent += connection.send(data[bytes_sent:])


def forward_message(data, sender_address):
    global connections

    #TODO: decrypt data using sender key

    for connection in connections:
        #TODO: encrypt data using recipient key

        # skip forwarding message to original sender
        if connection["host"]==sender_address:
            continue

        send_thread = threading.Thread(target=send_message, args=(connection["socket"], data))
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

    except Exception:
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
        client["host"] = address_info[0]
        client["socket"] = conn_sock
        connections.append(client)

        recv_thread = threading.Thread(target=recv_messages, args=(conn_sock, address_info[0]))
        recv_thread.start()

def terminate():
    print("Bye bye!")
    exit()

def main():
    # options, args = parse_args()

    try:
        host = "192.168.56.1"
        port = 890

        """
        for option, arg in options, args:
            if option=="-host":
                host = arg

            if option=="-port":
                port = arg
        """
        
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