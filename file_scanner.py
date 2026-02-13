import os
from config import SUPPORTED_EXTENSIONS


def scan_folder(folder_path):

    files = []

    for root, dirs, filenames in os.walk(folder_path):
        for file in filenames:

            if any(file.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS):
                files.append(os.path.join(root, file))

    return files
