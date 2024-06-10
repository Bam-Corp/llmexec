import re
import ast


def preprocess_code(code: str) -> str:
    # Remove any leading or trailing whitespace
    code = code.strip()

    # Check if the code is in the format ```python\n{CODE}``` or ```\n{CODE}
    match = re.search(r"```(python)?\n(.*?)```", code, re.DOTALL)
    if match:
        code = match.group(2).strip()

    # Check if the code is in the format `python\n{CODE}` (without backticks)
    if code.startswith("python\n"):
        code = code[7:].strip()

    # Check if the code is valid Python code
    if is_valid_python(code):
        return code

    # If no valid code format is found, return an empty string
    return ""

def is_valid_python(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False