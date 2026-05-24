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

    def do_POST(self):
        if self.path == "/upload":
            self.upload_file()

    def list_page(self):
        files = os.listdir(SHARED_FOLDER)
        html = "<html><body>"
        html += "<h2>Simple Files</h2>"
        html += """
        <form method="POST" action="/upload" enctype="multipart/form-data">
            <input name="file" type="file" />
            <input type="submit" value="Upload" />
        </form>
        <hr>
        """
        html == "<h3>Files</h3><ul>"
        for f in files:
            html += f'<li><a href="{f}">{f}</a></li>'

        html += "</ul></body></html>"

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

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