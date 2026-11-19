# port_scanner.py
# A simple TCP port scanner. It asks for a target and a list or range of ports,
# tries to connect to each port, and reports which ports are OPEN or CLOSED.

import socket                                                                                             # Bring in Python's built-in "socket" library, which lets programs talk over a network.
import time                                                                                               # Bring in the "time" library so we can measure how long the scan takes.

TIMEOUT = 0.5                                                                                             # How many seconds to wait for each port to answer before giving up and calling it closed.


def parse_ports(port_text):                                                                               # Define a function that turns the user's typed ports (like "21,22,80" or "1-100") into a list of numbers.
    if "-" in port_text:                                                                                  # Check if the user typed a range using a dash, like "1-100".
        start_text, end_text = port_text.split("-")                                                       # Split the text at the dash into a start number and an end number.
        ports = list(range(int(start_text), int(end_text) + 1))                                           # Build a list of every port from the start number up to and including the end number.
    else:                                                                                                 # Otherwise the user typed single ports separated by commas, like "21,22,80,443".
        ports = [int(piece) for piece in port_text.split(",")]                                            # Split the text at each comma and turn every piece into a whole number.
    if not ports:                                                                                         # If the list is empty (for example "100-1", where start is bigger than end), the input is invalid.
        raise ValueError("empty port list")                                                               # Raise an error so the main program knows the input was bad.
    for port in ports:                                                                                    # Look at every port number in the list one at a time.
        if port < 1 or port > 65535:                                                                      # Real port numbers only go from 1 to 65535, so anything outside that is invalid.
            raise ValueError("port out of range")                                                         # Raise an error so the main program knows the input was bad.
    return ports                                                                                          # Hand the finished list of port numbers back to whoever called this function.


def scan_port(ip_address, port):                                                                          # Define a function that checks ONE port and returns True if it is open or False if it is closed.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as scanner_socket:                             # Create a new TCP socket (IPv4 + TCP). "with" closes it automatically when we are done.
        scanner_socket.settimeout(TIMEOUT)                                                                # Set the time limit so we don't wait forever on a port that never answers.
        result = scanner_socket.connect_ex((ip_address, port))                                            # Try to connect. connect_ex returns 0 if the connection worked, or an error number if it failed.
    return result == 0                                                                                    # Return True if the result was 0 (port is open), otherwise False (port is closed).


def main():                                                                                               # Define the main function that holds all of the scanner's steps.
    target = input("Enter target host (example: 127.0.0.1 or scanme.nmap.org): ").strip()                 # Ask the user which computer to scan and remove any extra spaces they typed.
    port_text = input("Enter ports (example: 21,22,80,443 or 1-100): ").strip()                           # Ask the user which ports to scan.

    try:                                                                                                  # Try to turn the typed ports into a list of numbers.
        ports = parse_ports(port_text)                                                                    # Call our helper function to build the list of ports.
    except ValueError:                                                                                    # This runs if the ports were not valid whole numbers between 1 and 65535.
        print("Error: Invalid port input. Use whole numbers from 1 to 65535, like 21,22,80 or 1-100.")    # Tell the user what went wrong and show the correct format.
        return                                                                                            # Stop the program here because we can't scan without valid ports.

    try:                                                                                                  # Try to look up the target's IP address (this turns a name like scanme.nmap.org into numbers).
        ip_address = socket.gethostbyname(target)                                                         # Ask the computer's DNS system for the IP address of the target.
    except socket.gaierror:                                                                               # This runs if the host name doesn't exist or can't be found on the network.
        print(f"Error: Could not find host '{target}'. Check the spelling and your network connection.")  # Tell the user the host could not be found.
        return                                                                                            # Stop the program here because there is nothing to scan.

    print("-" * 50)                                                                                       # Print a divider line to make the output easier to read.
    print(f"Scanning {target} ({ip_address})")                                                            # Show which target and IP address we are about to scan.
    print(f"Ports to scan: {len(ports)}")                                                                 # Show how many ports we are going to check.
    print("-" * 50)                                                                                       # Print another divider line.

    start_time = time.perf_counter()                                                                      # Record the starting time so we can measure how long the scan takes.
    open_ports = []                                                                                       # Create an empty list to collect every open port we find.

    try:                                                                                                  # Try to scan all the ports, and catch any problems that happen along the way.
        for port in ports:                                                                                # Go through each port in the list one at a time.
            if scan_port(ip_address, port):                                                               # Check the port. If scan_port says it is open...
                print(f"Port {port:>5}: OPEN")                                                            # ...tell the user this port is OPEN.
                open_ports.append(port)                                                                   # ...and add it to our list of open ports.
            else:                                                                                         # Otherwise the port did not accept the connection...
                print(f"Port {port:>5}: closed")                                                          # ...so tell the user this port is closed.
    except KeyboardInterrupt:                                                                             # This runs if the user stops the scan early by pressing Ctrl+C.
        print("\nScan stopped by user.")                                                                  # Tell the user the scan was stopped on purpose.
    except OSError as error:                                                                              # This runs if a network problem happens during the scan (for example, the network goes down).
        print(f"Network error during scan: {error}")                                                      # Show a friendly message along with the actual error details.

    elapsed = time.perf_counter() - start_time                                                            # Work out how many seconds the scan took by subtracting the start time from the current time.
    print("-" * 50)                                                                                       # Print a divider line before the summary.
    print(f"Time taken:    {elapsed:.2f} seconds")                                                        # Show how long the scan took, rounded to 2 decimal places.
    print(f"Open ports:    {open_ports if open_ports else 'None'}")                                       # Show the list of open ports, or "None" if we didn't find any.
    print("-" * 50)                                                                                       # Print a final divider line.


if __name__ == "__main__":                                                                                # Only run main() if this file is run directly.
    main()  
