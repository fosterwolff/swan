import socket
import os

# Define the directory where HTML files are stored
html_dir = "C:\\Projects\\swan\\swan_site\\"

# Define the host and port
HOST = '127.0.0.1'
PORT = 8000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}...")

def handle_request(client_socket):
    try:
        # Receive the HTTP request from the client (max 1024 bytes)
        request = client_socket.recv(1024).decode()

        # Get the requested file from the URL (i.e., after GET)
        requested_file = request.split()[1]

        # Default to serving the index.html file if no specific file is requested
        if requested_file == "/":
            requested_file = "/index.html"

        # Define the full path to the requested file
        file_path = os.path.join(html_dir, requested_file.lstrip('/'))

        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()

            # Send the HTTP response with status code 200 and the file content
            response = f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{content}"
        else:
            # If file doesn't exist, return a 404 error
            response = "HTTP/1.1 404 Not Found\nContent-Type: text/html\n\n<h1>404 Not Found</h1>"

        # Send the response to the client
        client_socket.sendall(response.encode())

    except Exception as e:
        print(f"Error handling request: {e}")
        client_socket.sendall("HTTP/1.1 500 Internal Server Error\nContent-Type: text/html\n\n<h1>500 Internal Server Error</h1>")

    finally:
        # Close the client socket after handling the request
        client_socket.close()

# Main server loop
while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Handle the request from the client
    handle_request(client_socket)
