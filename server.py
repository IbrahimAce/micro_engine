# server.py  (Phase 2 version)
# Now uses the Request class to parse the raw bytes into a structured object.

import socket
from request import Request

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", 8080))
    server_socket.listen(5)

    print("=" * 50)
    print("Phase 2: HTTP parser server")
    print("Listening on http://127.0.0.1:8080")
    print("Press Ctrl+C to stop")
    print("=" * 50)

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(4096)

        if data:
            req = Request(data)
            print(f"\nMethod  : {req.method}")
            print(f"Path    : {req.path}")
            print(f"Headers : {req.headers}")
            if req.body:
                print(f"Body    : {req.body.decode('utf-8', errors='replace')}")

        response = b"HTTP/1.1 200 OK\r\nContent-Length: 14\r\n\r\nPhase 2 works!"
        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    run_server()
