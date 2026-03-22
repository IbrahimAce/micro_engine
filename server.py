# server.py  (Phase 3 version)
# Now uses the Router to find and call the right handler function.

import socket
from request import Request
from app import app   # import the router instance from app.py

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 8080))
    server_socket.listen(5)

    print("=" * 50)
    print("Phase 3: Routing engine server")
    print("Listening on http://127.0.0.1:8080")
    print("Registered routes:")
    for key in app.routes:
        print(f"  {key[0]} {key[1]}")
    print("Press Ctrl+C to stop")
    print("=" * 50)

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(4096)

        if not data:
            client_socket.close()
            continue

        req = Request(data)
        print(f"\n{req.method} {req.path}")

        # Ask the router for the handler function
        handler = app.get_handler(req.method, req.path)

        if handler is not None:
            # Call the handler and get the response body
            result = handler(req)
            status_line = b"HTTP/1.1 200 OK"
        else:
            result = f"404 Not Found: {req.path}"
            status_line = b"HTTP/1.1 404 Not Found"

        # Convert result to bytes if it isn't already
        if isinstance(result, bytes):
            body = result
        else:
            body = result.encode("utf-8")

        response = (
            status_line + b"\r\n"
            b"Content-Type: text/plain\r\n"
            b"Content-Length: " + str(len(body)).encode() + b"\r\n"
            b"\r\n"
        ) + body

        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    run_server()
