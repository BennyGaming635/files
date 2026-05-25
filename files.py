import http.server
import socketserver
import socket
import os
import cgi

PORT = 8000
SHARED_FOLDER = "SHARED"

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.home()
            return

        if self.path.startswith("/icons/"):
            icon_path = self.path.lstrip("/")
            full_path = os.path.join(icon_path)

            if os.path.exists(full_path):
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()

                with open(full_path, "rb") as f:
                    self.wfile.write(f.read())
            return

        file_path = self.path.lstrip("/")
        full_path = os.path.join(SHARED_FOLDER, file_path)

        if os.path.isfile(full_path):
            try:
                with open(full_path, "rb") as f:
                    self.send_response(200)

                    self.send_header(
                        "Content-Type",
                        "application/octet-stream"
                    )
                    self.send_header(
                        "Content-Disposition",
                        f'attachment; filename="{os.path.basename(full_path)}"'
                    )
                    self.end_headers()

                    self.wfile.write(f.read())

            except BrokenPipeError:
                pass

            return

        self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == "/upload":
            self.upload()
        elif self.path == "/delete":
            self.delete_file()

    def home(self):
        files = os.listdir(SHARED_FOLDER)

        html = """
        <html>
        <head>
        <title>Simple Files</title>
        <style>
            body {
                font-family: Arial;
                background: #0f172a;
                color: white;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: auto;
            }
            .card {
                background: #1e293b;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 20px;
            }
            input[type=file] {
                padding: 10px;
                background: #334155;
                border-radius: 8px;
                color: white;
            }
            input[type=submit] {
                padding: 10px 15px;
                background: #22c55e;
                border: none;
                border-radius: 8px;
                color: white;
                cursor: pointer;
                margin-left: 10px;
            }
            ul {
                list-style: none;
                padding: 0;
            }
            li {
                background: #334155;
                margin: 8px 0;
                padding: 10px;
                border-radius: 8px;
            }
            a {
                color: #60a5fa;
                text-decoration: none;
            }
            li {
                display: flex;
                align-items: center;
            }
            img {
                width: 20px;
                height: 20px;
            }
            .drop-zone {
                border: 2px dashed #475569;
                border-radius: 12px;
                padding: 40px;
                text-align: center;
                background: #0f172a;
                transition: 0.2s;
            }
            .drop-zone.dragover {
                background: #1e293b;
                border-color: #60a5fa;
            }
            .drop-zone p {
                margin: 0 0 15px 0;
                color: #94a3b8;
            }
            button {
                padding: 10px 15px;
                background: #22c55e;
                border: none;
                border-radius: 8px;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background: #16a34a;
            }
        </style>
        </head>

        <body>
        <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const uploadForm = document.getElementById('uploadForm');

        dropZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZone.classList.add("dragover");
        });

        dropZone.addEventListener("dragleave", () => {
            dropZone.classList.remove("dragover");
        });

        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.classList.remove("dragover");
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                uploadForm.submit();
            }
        });
        
        fileInput.addEventListener("change", () => {
            uploadForm.submit();
        });
        </script>
        <div class="container">

            <div class="card">
                <h2>Simple Files</h2>
                <p>Upload and share files easily</p>
            </div>

            <div class="card">
                <div class="drop-zone" id="dropZone">
                    <p>Drag and drop files here</p>
                    <form id="uploadForm" action="/upload" method="POST" enctype="multipart/form-data">
                        <input type="file name="file" id="fileInput" hidden>
                        <button type="button" onclick="document.getElementById('fileInput').click()">
                    Choose File
                </button>
                </form>
            </div>

            <div class="card">
                <h3>Files</h3>
                <ul>
        """

        for f in files:
            icon = get_icon(f)

            html += f"""
            <li>
                <img src="icons/{icon}" width="20" style="margin-right:10px; vertical-align:middle;">
                <a href="/{f}">{f}</a>

                <form method="POST" action="/delete" style="display:inline;">
                    <input type="hidden" name="filename" value="{f}">
                    <button type="submit"
                        style="margin-left:10px; background:#ef4444; border:none; color:white; padding:5px 10px; border-radius:6px; cursor:pointer;">
                        Delete
                    </button>
                </form>
            </li>
            """
        html += """
                </ul>
            </div>

        </div>
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
    
    def delete_file(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()

        filename = data.split("=")[-1]
        filename = os.path.basename(filename)

        path = os.path.join(SHARED_FOLDER, filename)

        if os.path.exists(path):
            os.remove(path)

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

def get_icon(filename):
    ext = filename.lower().split(".")[-1]
    mapping = {
        "pdf": "pdf.png",
        "txt": "txt.png",
        "jpg": "jpg.png",
        "jpeg": "jpg.png",
        "png": "png.png",
        "gif": "png.png",
    }

    return mapping.get(ext, "file.png")


os.makedirs(SHARED_FOLDER, exist_ok=True)

ip = get_ip()

print("=" * 40)
print("SIMPLE FILES (UPLOADS ENABLED)")
print("=" * 40)
print(f"Folder: {SHARED_FOLDER}")
print(f"URL: http://{ip}:{PORT}")
print("=" * 40)

with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()