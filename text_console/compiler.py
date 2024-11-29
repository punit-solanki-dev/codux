from .utils import generate_file, process_execution, safe_decode, remove_file
from constants.languages_meta_data import LANGUAGE_META_DATA
import os
import copy


def code_compiler(language, code, inputt=""):
    file_dir_path, filename, extension = generate_file(language=language, code=code)

    language_data = copy.deepcopy(LANGUAGE_META_DATA[language])
    filepath = os.path.join(file_dir_path, f"{filename}{extension}")

    command_list = language_data["execution_command"]
    output, error, isTimeout = "", "", False

    if language_data["compilation_required"]:
        compiled_filepath = os.path.join(file_dir_path, filename)
        command_list.extend([compiled_filepath, filepath])
        comp_output, comp_error, _ = process_execution(command_list)

        if comp_error:
            return safe_decode(comp_output), safe_decode(comp_error), isTimeout
        else:
            output, error, isTimeout = process_execution(compiled_filepath, inputt)
    else:
        command_list.append(filepath)
        output, error, isTimeout = process_execution(command_list, inputt)

    remove_file(path=file_dir_path)
    return safe_decode(output), safe_decode(error), isTimeout
