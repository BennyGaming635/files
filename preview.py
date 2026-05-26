import os

IMAGE_EXTS = {"png", "jpg", "jpeg", "gif", "webp"}

def is_previewable(filename):
    ext = filename.lower().split(".")[-1]
    return ext in IMAGE_EXTS