# References
# https://docs.python.org/3/howto/sockets.html 
# - used as reference for select.select()
# 
# https://stackoverflow.com/questions/14388706/how-do-so-reuseaddr-and-so-reuseport-differ 
# - used as reference for SO_REUSEADDR
# 
# https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/ 
# - used as reference for select.select() and SO_REUSEADDR

import sys
import socket
import select
import argparse

# Command line arguments to specify port number and verbose output
parser = argparse.ArgumentParser(description="A TCP chat server")

parser.add_argument("-p", "--port", dest="port", type=int, default=12345,
                    help="TCP port the server is listening on (default 12345)")
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                    help="turn verbose output on")
args = parser.parse_args()


# Open socket, make socket REUSEADDR, and bind it to a port(default 12345)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind(('', args.port))
except OSError:
    print("Error: Port is already in use")
except OverflowError:
    print("Error: Port range exceeded")

# Listen for connections
server.listen()

# List of sockets from which to read
socks = [server]

while True:
    try:
        read_sock, _, exception_sock = select.select(socks, [], socks)
        for sock in read_sock:
            # If the socket that is ready to read from is the main one, accept the new connection
            if sock == server:
                client, address = server.accept()

                # If verbose is enabled, print ip and port number of established connection
                if args.verbose:
                    print("Connection established with " + str(client.getpeername()))

                # Add the new client socket to the socks list
                socks.append(client)
                client.send("Thank you for connecting".encode('utf8'))
            
            # The socket is an already connected client socket, so receiving message
            else:
                message = sock.recv(1024).decode('utf8')

                # If verbose is enabled, print ip and port number from which message is being received
                if args.verbose:
                    print("Receiving message from " + str(sock.getpeername()))

                # If the message is bad, then remove the socket from the list
                if not message:
                    socks.remove(sock)

                    # If verbose is enabled, print ip and port number of the disconnected client
                    if args.verbose:
                        print(str(sock.getpeername())+ " disconnected")

                # Looping through socks to send message to all sockets except server
                for receiving_sock in socks:
                    if receiving_sock != sock and receiving_sock != server:
                        receiving_sock.send(message.encode('utf8'))

                        # If verbose is enabled, print ip and port number to which message is being sent
                        if args.verbose:
                            print("Sending message to " + str(receiving_sock.getpeername()))

    # If Ctrl+C, then shut down server                        
    except KeyboardInterrupt:
        print("Shutting down the server")
        sys.exit(0)