import http.server
import socketserver
import socket
import os

SHARED_FOLDER = "shared"
PORT = 8000

os.makedirs(SHARED_FOLDER, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path =="/":
            self.list_page()
        else:
            super().do_GET()

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    print("=" * 40)
    print("Files | The simple file server")
    print("=" * 40)
    print(f"Serving your simple files in: {os.getcwd()}")
    print()
    print("Open this on other devices:")
    print(f"http://{local_ip}:{PORT}")
    print("=" * 40)

    httpd.serve_forever()