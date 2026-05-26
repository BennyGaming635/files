import os

IMAGE_EXTS = {"png", "jpg", "jpeg", "gif", "webp"}

def is_previewable(filename):
    ext = filename.lower().split(".")[-1]
    return ext in IMAGE_EXTS

def render_preview(file_path):
    return """
    <html>
    <head>
        <title>Preview</title>
        <style>
            body {
                margin: 0;
                background: #0f172a;
                color: white;
                font-family: Arial;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }
            
            img {
                max_width: 90%;
                max_height: 80vh;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            }
            
            a {
                margin-top: 20px;
                color: #60a5fa;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <img src="/__FILE_PATH__">
        <a href="/__FILE_PATH__" download>Download</a>
    </body>
    </html>
    """
    return replace("/__FILE_PATH__", file_path)