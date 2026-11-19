# server.py
# This is the SERVER script. It waits for a client to connect,
# receives a message from the client, and sends a reply back.
# Run this script first, before running client.py.

import socket                                                                               # Bring in Python's built-in "socket" library, which lets programs talk over a network.

HOST = "127.0.0.1"                                                                          # The IP address the server will listen on. "127.0.0.1" (localhost).
PORT = 65432                                                                                # The port number the server will listen on.


def main():                                                                                 # Define the main function that holds all of the server's steps.
    try:                                                                                    # Try to run the server steps, and catch any problems that happen.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:            # Create a new socket. AF_INET means IPv4 addresses, SOCK_STREAM means TCP (a reliable connection). The socket closes automatically.
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)             # Allow the port to be reused right away if we restart the server, instead of waiting for the OS to free it.
            server_socket.bind((HOST, PORT))                                                # Attach the socket to our chosen IP address and port so clients know where to find it.
            server_socket.listen(1)                                                         # Start listening for incoming connections. The 1 means up to 1 client can queue.
            print(f"Server is listening on {HOST}:{PORT} ...")                              # Tell the user the server is ready and where it is listening.

            client_socket, client_address = server_socket.accept()                          # Pause here until a client connects. When one does, we get a new socket for that client and its address.
            with client_socket:                                                             # Use "with" again so the client's connection is automatically closed when we are done.
                print(f"Connected to client at {client_address}")                           # Tell the user which client connected (its IP address and port).
                data = client_socket.recv(1024)                                             # Receive up to 1024 bytes of data sent by the client.
                print(f"Received from client: {data.decode()}")                             # Turn the received bytes into normal text and show it on the screen.
                client_socket.sendall("Hello from the server! Message received.".encode())  # Send a reply back to the client. The text must be turned into bytes with encode() first.
                print("Reply sent to client. Closing connection.")                          # Tell the user that the reply was sent.

    except OSError as error:                                                                # This runs if the port is already being used by another program or can't be opened.
        print(f"Server error (is the port already in use?): {error}")                       # Show a message along with the actual error details.
    except KeyboardInterrupt:                                                               # This runs if the user stops the server by pressing Ctrl+C.
        print("\nServer stopped by user.")                                                  # Tell the user the server was stopped on purpose.


if __name__ == "__main__":                                                                  # Only run main() if this file is run directly (not if it is imported into another script).
    main()                                                                                  # Start the server.
