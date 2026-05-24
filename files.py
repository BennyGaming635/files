import http.server
import socketserver
import socket
import os

SHARED_FOLDER = "shared"
PORT = 8000

os.makedirs(SHARED_FOLDER, exist_ok=True)
os.chdir(SHARED_FOLDER)

hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
Handler = http.server.SimpleHTTPRequestHandler