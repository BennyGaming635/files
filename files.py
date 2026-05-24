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

    def upload_file(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"],
            },
        )

        file_item = form["file"]

        if file_item.filename:
            filename = os.path.basename(file_item.filename)
            path = os.path.join(SHARED_FOLDER, filename)

            with open(path, "wb") as f:
                f.write(file_item.file.read())

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()
    
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except:
        return "127.0.0.1"
    finally:
        s.close()

ip = get_ip()

print("=" * 40)
print("Simple Files | UPLOADS ARE ENABLED")
print("=" * 40)
print(f"http://{ip}:{PORT}")
print("=" * 40)

os.chdir(SHARED_FOLDER)
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()