import http.server
import socketserver
import socket
import os
import cgi

PORT = 8000
SHARED_FOLDER = "SHARED"

os.makedirs(SHARED_FOLDER, exist_ok=True)

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.home()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/upload":
            self.upload()

    def home(self):
        files = os.listdir(SHARED_FOLDER)

        html = """
        <html>
        <head>
        <title>Simple Files</title>
        </head>
        <body>
        <h2>All Files</h2>

        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="Upload">
        </form>

        <hr>
        <h3>Files</h3>
        <ul>
        """

        for f in files:
            html += f'<li><a href="/{f}">{f}</a></li>'

        html += """
        </ul>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


    def upload(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": self.headers["Content-Type"],
            },
        )

        if "file" not in form:
            self.send_response(400)
            self.end_headers()
            return

        file_item = form["file"]

        if file_item.filename:
            filename = os.path.basename(file_item.filename)
            filepath = os.path.join(SHARED_FOLDER, filename)

            with open(filepath, "wb") as f:
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


os.makedirs(SHARED_FOLDER, exist_ok=True)
os.chdir(SHARED_FOLDER)

ip = get_ip()

print("=" * 40)
print("SIMPLE FILES (UPLOADS ENABLED)")
print("=" * 40)
print(f"Folder: {SHARED_FOLDER}")
print(f"URL: http://{ip}:{PORT}")
print("=" * 40)

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()