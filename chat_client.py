import socket
import threading
import argparse
import sys
import signal

# Command line arguments to specify name, ip address, port number, and verbose output
parser = argparse.ArgumentParser(description="A TCP chat client")

parser.add_argument("-n", "--name", dest="name", default=socket.gethostname(), help="name to be prepended in messages (default: machine name)")
parser.add_argument("-s", "--server", dest="server", default="127.0.0.1",
                    help="server hostname or IP address (default: 127.0.0.1)")
parser.add_argument("-p", "--port", dest="port", type=int, default=12345,
                    help="TCP port the server is listening on (default 12345)")
parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                    help="turn verbose output on")
args = parser.parse_args()

# Connect to the server and send client's name
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((args.server, args.port))
#client.send(args.name.encode('utf8'))

# if verbose printing is enabled
if args.verbose:
    print("Connection established with server at {args.server}:{args.port}")

# The receive() and write() functions were adapted from
# https://www.neuralnine.com/tcp-chat-in-python/

# Listen to server and print message
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf8')
            #if verbose printing is enabled
            if args.verbose:
                print(f"Receiving message from {args.server}:{args.port}")
            print(message)

        except UnicodeDecodeError:
            print("Error: Can't decode message")

        if not message:
            # Close connection when connection to server is lost
            print("Server connection lost")
            client.close()
            break

# Send messages to the server
def write():
    while True:
        message = '{}: {}'.format(args.name, input(''))

        # if verbose printing is enabled
        if args.verbose:
            print(f"Sending message to {args.server}:{args.port}")

        client.send(message.encode('utf8'))

# The code for multithreading was adapted from
# https://stackoverflow.com/questions/2846653/how-can-i-use-threading-in-python

# Starting listening thread
receive_thread = threading.Thread(target = receive)
# Making the thread a daemon so that it ends whenever the main thread ends
receive_thread.daemon = True
# Starting the thread
receive_thread.start()

# Function to exit chat client when user enters CTRL+C
def sigint_handler(signal, frame):
    print ("Shutting down the chat client")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

# Write function
write()