from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.formatters import convert_to_python_raw_string, convert_to_raw_string
from code_analyzer.python_analyzer import is_code_not_safe
from .compiler import code_compiler
from .utils import generate_python_error_body
import json

text_executor = APIRouter()


@text_executor.post("/execute-text", response_class=JSONResponse)
async def execute_text(request: Request):
    data = json.loads(await request.body())
    language = data["language"].upper().strip()
    if language == "PYTHON":
        code = convert_to_python_raw_string(data["code"])
        inputt = convert_to_python_raw_string(data["input"])
    else:
        code = convert_to_raw_string(data["code"])
        inputt = convert_to_raw_string(data["input"])

    if language == "PYTHON":
        restricted_code, message = is_code_not_safe(language, code)
        if restricted_code:
            return {"message": message, "warning": True}

    output, error, isTimeout = code_compiler(language, code, inputt)

    if isTimeout:
        return {
            "message": "Time Limit Exceed! Code is taking too long to execute.",
            "error": True,
        }
    elif error:
        return {"message": generate_python_error_body(error), "error": True}

    return {"message": output}
