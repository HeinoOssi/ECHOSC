import socket
import sys
import argparse
from _thread import *
import threading

print_lock = threading.Lock()

host = 'localhost'
data_payload = 2048
backlog = 5

def echo_server(port):
    # TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    # Bind socket 2 port
    server_address = (host,port)
    print("Starting echo server on %s port %s" % server_address)
    sock.bind(server_address)

    # Listen to clients, max # of queued connections = backlog
    sock.listen(backlog)

    while True:
        print("Waiting for a message from client")
        client, address = sock.accept()

        # Lock acquired by client
        print_lock.acquire()

        print("Connected: ", address[0], ":", address[1])

        # Start a new thread
        start_new_thread(threaded, (client,))
           
    # Close connection
    sock.close()

def threaded(client):
    while True:
        # Data received from client
        data = client.recv(data_payload)

        if data:
            # Convert received data to string
            data_to_string = data.decode()
            print("Received data: %s" % data_to_string)

            # Send data back
            client.send(data)

        if not data:
            print("Closing")
            # Release lock on exit
            print_lock.release()

    client.close()   

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description='Socket server example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)
