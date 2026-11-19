# client.py
# This is the CLIENT script. It connects to the server, sends a message,
# and prints the reply that the server sends back.
# Run this script second, after server.py is already running.

import socket                                                                     # Bring in Python's built-in "socket" library, which lets programs talk over a network.

HOST = "127.0.0.1"                                                                # The IP address of the server we want to reach. "127.0.0.1" (localhost).
PORT = 65432                                                                      # The port number the server is listening on. This must match the PORT in server.py.


def main():                                                                       # Define the main function that holds all of the client's steps.
    try:                                                                          # Try to run the client steps, and catch any problems that happen along the way.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  # Create a new socket. AF_INET means IPv4 addresses, SOCK_STREAM means TCP (a reliable connection). The socket closes automatically.
            client_socket.settimeout(5)                                           # Set a 5-second time limit so the client doesn't wait forever if the server never answers.
            client_socket.connect((HOST, PORT))                                   # Connect to the server at the given IP address and port.
            print(f"Connected to server at {HOST}:{PORT}")                        # Tell the user the connection worked.
            client_socket.sendall("Hello from the client!".encode())              # Send a message to the server. The text must be turned into bytes with encode() first.
            reply = client_socket.recv(1024)                                      # Wait for the server's reply and receive up to 1024 bytes of it.
            print(f"Received from server: {reply.decode()}")                      # Turn the reply bytes back into normal text and show it on the screen.

    except ConnectionRefusedError:                                                # This runs if nothing is listening on that port (check server.py)
        print("Connection refused. Make sure server.py is running first.")        # Tell the user what most likely went wrong and how to fix it.
    except socket.timeout:                                                        # This runs if the server takes longer than 5 seconds to respond.
        print("Connection timed out. The server did not respond in time.")        # Tell the user the connection attempt timed out.
    except OSError as error:                                                      # This catches any other network-related error (for example, a bad address).
        print(f"Client error: {error}")                                           # Show a friendly message along with the actual error details.


if __name__ == "__main__":                                                        # Only run main() if this file is run directly.
    main()                                                                        # Start the client.
