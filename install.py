import os
import shutil
from pathlib import Path


def replace_text_in_files(root_dir, old_text, new_text):
    hyphen_name = new_text.lower()
    hyphen_name = hyphen_name.replace(" ", "-")
    hyphen_name = hyphen_name.replace("_", "-")

    underscore_name = new_text.lower()
    underscore_name = underscore_name.replace(" ", "_")
    underscore_name = underscore_name.replace("-", "_")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith((".py", ".yaml", ".toml", "Dockerfile", "txt")):
                continue

            file_path = os.path.join(dirpath, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                filedata = file.read()

            if old_text not in filedata:
                continue

            new_filedata = filedata.replace(old_text, new_text)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_filedata)


def replace_folder_names(root_dir, old_name, new_name):
    new_name = new_name.lower()
    new_name = new_name.replace(" ", "_")
    new_name = new_name.replace("-", "_")

    for dirpath, dirnames, _ in os.walk(root_dir, topdown=False):
        for dirname in dirnames:
            if dirname != old_name:
                continue

            current_dir = os.path.join(dirpath, dirname)
            new_dir_path = os.path.join(dirpath, new_name)

            counter = 1
            final_new_dir_path = new_dir_path
            while os.path.exists(final_new_dir_path):
                final_new_dir_path = f"{new_dir_path}_{counter}"
                counter += 1

            shutil.move(current_dir, final_new_dir_path)
            print(f"Renamed '{current_dir}' to '{final_new_dir_path}'")


root_directory = Path(__file__).resolve().parent
replace_text_in_files(root_directory, "unknown", "unknown")
replace_folder_names(root_directory, "unknown", "unknown")
