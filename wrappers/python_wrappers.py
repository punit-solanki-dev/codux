from typing import List


class PythonCodeWrapper:
    DEPENDENCIES_DATA = {
        "print": "builtins",
        "input": "builtins",
        # Add more built-in functions here as needed
    }

    def __init__(self, code: str):
        """
        Initializes the PythonCodeWrapper with the provided code.

        :param code: The code to be wrapped.
        """
        self.code = code

    def wrap_all(self) -> str:
        """
        Wraps the code with all available dependency wrappers.

        :return: The wrapped code as a string.
        """
        wrapped_code = self.import_and_wrap(list(self.DEPENDENCIES_DATA.keys()))
        return f"{wrapped_code}\n{self.code}"

    @staticmethod
    def wrap_in_modules(code: str, wrapped_in: List[str]) -> str:
        """
        Wraps the code with specified dependency wrappers.

        :param code: The code to be wrapped.
        :param wrapped_in: List of functions to wrap.
        :return: The wrapped code or an error message.
        """
        unsupported_modules = [
            module
            for module in wrapped_in
            if module not in PythonCodeWrapper.DEPENDENCIES_DATA
        ]
        if unsupported_modules:
            return (
                f"Wrapper does not support {unsupported_modules} function(s) at the moment. "
                f"Supported functions are: {list(PythonCodeWrapper.DEPENDENCIES_DATA.keys())}"
            )

        wrapped_code = PythonCodeWrapper.import_and_wrap(wrapped_in)
        return f"{wrapped_code}\n{code}"

    @staticmethod
    def import_and_wrap(wrapped_in: List[str]) -> str:
        """
        Generates import statements and wraps the specified dependencies.

        :param wrapped_in: List of functions to wrap.
        :return: Import and wrapper code as a string.
        """
        imports = set()
        wrapper_code = []

        for function in wrapped_in:
            if function in PythonCodeWrapper.DEPENDENCIES_DATA:
                module = PythonCodeWrapper.DEPENDENCIES_DATA[function]
                imports.add(f"import {module}")
                wrapper_code.append(PythonCodeWrapper.call_wrapper(function))

        return "\n".join(imports) + "\n" + "\n".join(wrapper_code)

    @staticmethod
    def call_wrapper(function: str) -> str:
        """
        Returns the wrapper function for the specified built-in function.

        :param function: The built-in function to wrap.
        :return: The wrapper code as a string.
        """
        wrapper_method = getattr(PythonCodeWrapper, f"{function}_wrapper", None)
        return wrapper_method() if wrapper_method else ""

    @staticmethod
    def print_wrapper() -> str:
        """
        Creates a custom print wrapper.

        :return: The print wrapper code as a string.
        """
        return """original_print = builtins.print
def custom_print(*args, **kwargs):
    kwargs["flush"] = True
    original_print(*args, **kwargs)
builtins.print = custom_print
"""

    @staticmethod
    def input_wrapper() -> str:
        """
        Creates a custom input wrapper.

        :return: The input wrapper code as a string.
        """
        return """original_input = builtins.input
def custom_input(prompt):
    print(prompt)
    return original_input()
builtins.input = custom_input
"""

    @staticmethod
    def add_custom_function(func_name: str, wrapper_code: str, module: str) -> None:
        """
        Dynamically adds a custom function wrapper.

        :param func_name: The name of the function to wrap.
        :param wrapper_code: The code of the custom wrapper.
        """
        PythonCodeWrapper.DEPENDENCIES_DATA[func_name] = module
        exec(wrapper_code, globals())


# Example usage:
# code = """
# print("Hello, world!")
# input("What is your name?")
# """

# wrapper = PythonCodeWrapper(code)
# wrapped_code = wrapper.all_wrap()
# print(wrapped_code)
