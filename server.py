# server.py
# A raw TCP socket server.
# It listens for connections, reads the raw bytes the browser sends,
# prints them so we can see what an HTTP request actually looks like,
# then sends back a simple response.

import socket

def run_server():
    # AF_INET = use IPv4 addresses
    # SOCK_STREAM = use TCP (reliable, connection-based)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # SO_REUSEADDR lets us restart the server quickly during development
    # without waiting for the OS to release the port
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind to localhost on port 8080
    server_socket.bind(("127.0.0.1", 8080))

    # Start listening — allow up to 5 queued connections
    server_socket.listen(5)

    print("=" * 50)
    print("Phase 1: Raw socket server")
    print("Listening on http://127.0.0.1:8080")
    print("Press Ctrl+C to stop")
    print("=" * 50)

    while True:
        # accept() blocks here — it waits until someone connects
        # client_socket is a new socket just for that one client
        # addr is a tuple of (ip_address, port)
        client_socket, addr = server_socket.accept()
        print(f"\nNew connection from {addr}")

        # recv(4096) reads up to 4096 bytes from the client
        data = client_socket.recv(4096)

        if data:
            print("\n--- RAW BYTES RECEIVED (decoded as text) ---")
            print(data.decode("utf-8", errors="replace"))
            print("--- END ---\n")

        # We must send a valid HTTP response or the browser shows an error
        # HTTP/1.1 200 OK  = status line
        # Content-Length   = how many bytes in the body
        # \r\n\r\n         = blank line separating headers from body
        response = b"HTTP/1.1 200 OK\r\nContent-Length: 11\r\n\r\nHello World"
        client_socket.sendall(response)

        # Close this client's connection
        client_socket.close()

if __name__ == "__main__":
    run_server()
