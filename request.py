# request.py
# Takes the raw bytes from the socket and turns them into a usable Python object.
#
# A real HTTP request looks like this:
#
#   GET /users HTTP/1.1\r\n
#   Host: localhost:8080\r\n
#   User-Agent: curl/7.88.1\r\n
#   \r\n
#   (body goes here if POST)
#
# \r\n means carriage-return + newline (Windows-style line ending that HTTP requires)
# The blank line (\r\n\r\n) separates the headers from the body.

class Request:
    def __init__(self, raw_data: bytes):
        self.raw      = raw_data   # original bytes
        self.method   = ""         # GET, POST, etc.
        self.path     = ""         # /users, /home, etc.
        self.headers  = {}         # {"Host": "localhost:8080", ...}
        self.body     = b""        # body bytes (for POST requests)

        self._parse()

    def _parse(self):
        try:
            # Decode bytes to a Python string
            text = self.raw.decode("utf-8", errors="replace")
        except Exception:
            return

        if not text:
            return

        # Split on the blank line that separates headers from body
        if "\r\n\r\n" in text:
            header_section, body_text = text.split("\r\n\r\n", 1)
            self.body = body_text.encode("utf-8")
        else:
            header_section = text

        # Split the header section into individual lines
        lines = header_section.split("\r\n")

        if not lines:
            return

        # --- Parse the request line (first line) ---
        # Example: "GET /users HTTP/1.1"
        request_line = lines[0].strip()
        parts = request_line.split(" ")
        if len(parts) >= 2:
            self.method = parts[0]   # "GET"
            self.path   = parts[1]   # "/users"

        # --- Parse the headers (remaining lines) ---
        # Example: "Host: localhost:8080"
        for line in lines[1:]:
            if ":" in line:
                # Split only on the first colon so values like "http://..." stay intact
                key, value = line.split(":", 1)
                self.headers[key.strip()] = value.strip()

    def __repr__(self):
        return f"<Request {self.method} {self.path}>"
