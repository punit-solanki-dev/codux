import codecs, re

def generate_python_error_body(error):
    try:
        split_value_1 = ".py:"
        split_value_2 = '.py", '
        err = error.split(split_value_1 if split_value_1 in error else split_value_2)[1]

        return f"ERROR!\nTraceback (most recent call last):\n  File <main.py>, {err}"
    except Exception:
        return error

def safe_decode(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value

def convert_to_python_raw_string(code):
    en_code = re.sub(
        r"(?<!r)(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"|\'(.*?)\'|\"(.*?)\")",
        lambda m: f"r{m.group(0)}",
        code,
        flags=re.DOTALL,
    )
    en_code.replace("\\", "\\\\")
    return codecs.decode(en_code, "raw_unicode_escape")

def convert_to_raw_string(code):
    en_code = re.sub(
        r"(?<!r)(\'\'\'(.*?)\'\'\'|\"\"\"(.*?)\"\"\"|\'(.*?)\'|\"(.*?)\")",
        lambda m: f"{m.group(0)}",
        code,
        flags=re.DOTALL,
    )
    en_code.replace("\\", "\\\\")
    return codecs.decode(en_code, "raw_unicode_escape")