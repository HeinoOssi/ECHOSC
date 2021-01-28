import sys
import socket
import argparse

host = 'localhost'

def echo_client(port):
    #create tcp/ip socket and connect it to the server
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = (host,port)
    sock.settimeout(4000)
    print("Connecting to %s port %s"%server_address)
    sock.connect(server_address)
    while True:
        # send data
        try:
            # ask for message to send, convert it to bytes and send it.
            message = str(input("Type message to send: "))
            message_to_bytes = str.encode(message)
            type(message_to_bytes)

            print("Sending: %s" %message)
            sock.sendall(message_to_bytes)

            # wait for response
            amount_received = 0
            amount_expected = len(message_to_bytes)
            while amount_received < amount_expected:
                data = sock.recv(16)
                amount_received += len(data)

                # convert received bytes back to string and print it
                data_to_string = data.decode()
                print("Received: %s" % data_to_string)

        except Exception as e:
            print("Error: %s" %str(e))
    #finally:
    print("Closing connection")
    sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Socket example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_client(port)