import os, shutil, uuid
from constants.languages_meta_data import LANGUAGE_META_DATA

def generate_file(language, code):
    extension = LANGUAGE_META_DATA[language]["extension"]
    filename = f"Main"
    dir_name = f"code_id_{uuid.uuid4()}"
    file_dir_path = f"code_files_dump/{language.lower()}/{dir_name}/"
    os.makedirs(file_dir_path, exist_ok=True)
    with open(os.path.join(file_dir_path, f"{filename}{extension}"), "w") as file:
        file.write(code)
    return file_dir_path, filename, extension

def remove_file(path):
    shutil.rmtree(path)
    return True