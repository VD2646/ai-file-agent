import os
import shutil
import re


def clean_folder_name(name):

    name = name.replace("*", "")

    name = re.sub(r'[<>:"/\\|?*]', '', name)

    return name.strip()


def move_file(file_path, base_folder, category):

    safe_category = clean_folder_name(category)

    target_folder = os.path.join(base_folder, safe_category)

    os.makedirs(target_folder, exist_ok=True)

    file_name = os.path.basename(file_path)

    shutil.move(file_path, os.path.join(target_folder, file_name))


def delete_empty_folders(folder_path):

    for root, dirs, files in os.walk(folder_path, topdown=False):

        if not dirs and not files:
            try:
                os.rmdir(root)
            except:
                pass
