import os

IMAGE_EXTS = {"png", "jpg", "jpeg", "gif", "webp"}
VIDEO_EXTS = {"mp4", "webm", "ogg"}

def is_image(filename):
    ext = filename.lower().split(".")[-1]
    return ext in IMAGE_EXTS

def is_video(filename):
    ext = filename.lower().split(".")[-1]
    return ext in VIDEO_EXTS

def render_image(file_path):
    return f"""
    <html>
    <head>
        <title>Preview</title>
        <style>
            body {{
                margin: 0;
                background: #0f172a;
                color: white;
                font-family: Arial;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }}

            img {{
                max-width: 90%;
                max-height: 80vh;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            }}

            a {{
                margin-top: 20px;
                color: #60a5fa;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <img src="/{file_path}?raw=1">
        <a href="/{file_path}" download>Download</a>
    </body>
    </html>
    """

def render_video(file_path):
    return f"""
    <html>
    <head>
        <title>Preview</title>
        <style>
            body {{
                margin: 0;
                background: #0f172a;
                color: white;
                font-family: Arial;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
            }}

            video {{
                max-width: 90%;
                max-height: 80vh;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            }}

            a {{
                margin-top: 20px;
                color: #60a5fa;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <video controls autoplay>
            <source src="/{file_path}=?raw=1" type="video/{file_path.split('.')[-1]}">
        </video>
        <a href="/{file_path}?download=1">Download</a>
    </body>
    </html>
    """