from subprocess import Popen, PIPE, TimeoutExpired
import uuid, os, shutil, re, codecs
from constants.languages_meta_data import LANGUAGE_META_DATA
from constants.error_messages import ErrorMessages


# def generate_wrapped_code(code):
#     wrapped_code_lines = [
#         "try:",
#         *["    " + line for line in code.splitlines()],
#         "except Exception as e:",
#         "    print(f'An error occurred: {e}')",
#     ]
#     return "\n".join(wrapped_code_lines)


def convert_to_raw_string(code):
    en_code = re.sub(
        r"(?<!r)(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"|\'(.*?)\'|\"(.*?)\")",
        lambda m: f"r{m.group(0)}",
        code,
        flags=re.DOTALL,
    )
    en_code.replace("\\", "\\\\")
    return codecs.decode(en_code, "raw_unicode_escape")


def generate_file(language, code):
    extension = LANGUAGE_META_DATA[language]["extension"]
    filename = f"Main"
    dir_name = f"code_id_{uuid.uuid4()}"
    file_dir_path = f"code_files_dump/{language.lower()}/{dir_name}/"
    os.makedirs(file_dir_path, exist_ok=True)
    with open(os.path.join(file_dir_path, f"{filename}{extension}"), "w") as file:
        file.write(code)
    return file_dir_path, filename, extension


def process_execution(command_list, inputt=""):
    process = Popen(command_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    process.stdin.write(bytes(inputt, "utf-8"))
    isTimeout = False
    try:
        output, error = process.communicate(timeout=180)
        process.stdin.close()
    except TimeoutExpired:
        output, error, isTimeout = None, ErrorMessages.PROCESS_TIMEOUT.value, True
        process.kill()
    except Exception as e:
        output, error = None, repr(e)
        process.kill()
    return output, error, isTimeout


def remove_file(path):
    shutil.rmtree(path)
    return True


def safe_decode(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def generate_python_error_body(error):
    try:
        split_value_1 = ".py:"
        split_value_2 = '.py", '
        err = error.split(split_value_1 if split_value_1 in error else split_value_2)[1]

        return f"ERROR!\nTraceback (most recent call last):\n  File <main.py>, {err}"
    except Exception:
        return error
