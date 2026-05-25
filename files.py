import http.server
from importlib.resources import files
import socketserver
import socket
import os
import cgi

PORT = 8000
SHARED_FOLDER = "SHARED"

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith("/?path=") or self.path == "/":
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
        elif self.path == "/mkdir":
            self.mkdir()

    def home(self):
        current_path = self.path.split("?path=")
        if len(current_path) > 1:
            current_path = current_path[1]
        else:
            current_path = ""

        safe_path = os.path.normpath(current_path)
        folder = os.path.join(SHARED_FOLDER, safe_path)
        os.makedirs(folder, exist_ok=True)

        files = os.listdir(folder)

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

            .section-title {
                font-size: 16px;
                font-weight: 600;
                margin-bottom: 12px;
                color: #e2e8f0;
            }

            .folder-form {
                display: flex;
                gap: 10px;
                align-items: center;
            }
            
            .folder-form input[type=text] {
                flex: 1;
                padding: 12px 14px;
                border-radius: 10px;
                border: 1px solid #334155;
                background: #0f172a;
                color: white;
                outline: none;
                transition: 0.2s;
                font-size: 14px;
            }

            .folder-form input[type=text]:placeholder {
                color: #94a3b8;
            }

            .folder-form input[type=text]:focus {
                border-color: #60a5fa;
                box-shadow: 0 0 0 3px rgba(96, 164, 250, 0.2);
            }

            .folder-form button {
                padding: 12px 16px;
                border-radius: 10px;
                border: none;
                background: #22c55e;
                color: white;
                cursor: pointer;
                font-weight: 500;
                transition: 0.2s;
            }

            .folder-form button:hover {
                background: #16a34a;
                transform: translateY(-1px);
            }

            .folder-form button:active {
                transform: translateY(0px);
            }

        </style>
        </head>

        <body>
        <div class="container">

            <div class="card">
                <h2>Simple Files</h2>
                <p>Upload and share files easily</p>
            </div>

            <div class="card">
                <div id="progressContainer" style="display:none; margin-top:15px;">
                    <div style="width:100%; background:#334155; border-radius:8px; overflow:hidden;">
                        <div id="progressBar"
                            style="height:12px; width:0%; background:#22c55e; transition:width 0.2s;">
                        </div>
                    </div>
                    <p id="progressText" style="color:#94a3b8; font-size:14px;"></p>
                </div>
                <div class="drop-zone" id="dropZone">
                    <p>Drag and drop files here</p>
                    <input type="hidden" name="path" value="__SAFE_PATH__">
                    <input type="file"
                        name="file"
                        id="fileInput"
                        hidden>
                    <button id="chooseBtn" type="button"
                            onclick="document.getElementById('fileInput').click()">
                        Choose File
                    </button>
                </div>
            </div>
            <div class="card">
                <form action="/mkdir" method="POST" class="folder-form">
                    <input type="text"
                        name="folder"
                        placeholder="New folder name"
                        required>
                    <input type="hidden"
                        name="path"
                        value="__SAFE_PATH__">
                    <button type="submit">
                        Create Folder
                    </button>
                </form>
            </div>

            <div class="card">
                <h3>Files</h3>
                <ul>
        """

        html = html.replace("__SAFE_PATH__", safe_path)

        for f in files:
            full_item = os.path.join(folder, f)
            if os.path.isdir(full_item):
                html += f"""
                <li>
                    📁
                    <a href="/?path={safe_path}/{f}">
                        {f}
                    </a>
                </li>
                """
            else:
                icon = get_icon(f)

                file_url = f"{safe_path}/{f}".strip("/")

                html += f"""
                <li>
                    <img src="/icons/{icon}" width="20">

                    <a href="/{file_url}">
                        {f}
                    </a>

                    <form method="POST" action="/delete" style="display:inline;">
                        <input type="hidden"
                            name="filename"
                            value="{file_url}">

                        <button type="submit">
                            Delete
                        </button>
                    </form>
                </li>
                """
        html += """
                </ul>
            </div>

        </div>
                <script>
        const dropZone = document.getElementById("dropZone");
        const fileInput = document.getElementById("fileInput");
        const chooseBtn = document.getElementById("chooseBtn");

        window.addEventListener("dragover", function(e) {
            e.preventDefault();
        });

        window.addEventListener("drop", function(e) {
            e.preventDefault();
        });

        chooseBtn.addEventListener("click", () => {
            fileInput.click();
        });

        async function uploadFile(file) {
        const formData = new FormData();
        formData.append("file", file);
        
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/upload");
        
        const progressBar = document.getElementById("progressBar");
        const progressText = document.getElementById("progressText");
        const progressContainer = document.getElementById("progressContainer");

        progressContainer.style.display = "block";
        progressBar.style.width = "0%";
        progressText.innerText = "Uploading... 0%";

        xhr.upload.onprogress = function (e) {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                progressBar.style.width = percent + "%";
                progressText.innerText = "Uploading... " + percent + "%";
            }
        };

        xhr.onload = function () {
            progressBar.style.width = "100%";
            progressText.innerText = "Upload complete!";
            setTimeout(() => location.reload(), 500);
        };

        xhr.send(formData);
        }

        fileInput.addEventListener("change", () => {
            if (fileInput.files.length > 0) {
                uploadFile(fileInput.files[0]);
            }
        });

        dropZone.addEventListener("dragover", () => {
            dropZone.classList.add("dragover");
        });

        dropZone.addEventListener("dragleave", () => {
            dropZone.classList.remove("dragover");
        });

        dropZone.addEventListener("drop", (e) => {
            dropZone.classList.remove("dragover");

            const files = e.dataTransfer.files;

            if (files.length > 0) {
                uploadFile(files[0]);
            }
        });
        </script>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def mkdir(self):
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()
        import urllib.parse
        
        parsed = urllib.parse.parse_qs(data)
        
        folder_name = parsed.get("folder", [""])[0]
        current_path = parsed.get("path", [""])[0]
        
        target = os.path.join(
            SHARED_FOLDER,
            current_path,
            folder_name
        )
        os.makedirs(target, exist_ok=True)
        self.send_response(303)
        self.send_header("Location", f"/?path={current_path}")
        self.end_headers()


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

        path = form.getvalue("path", "")

        upload_folder = os.path.join(
            SHARED_FOLDER,
            path
        )

        os.makedirs(upload_folder, exist_ok=True)

        if file_item.filename:
            filename = os.path.basename(file_item.filename)

            filepath = os.path.join(
                upload_folder,
                filename
            )

            with open(filepath, "wb") as f:
                f.write(file_item.file.read())

        self.send_response(303)
        self.send_header(
            "Location",
            f"/?path={path}"
        )
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