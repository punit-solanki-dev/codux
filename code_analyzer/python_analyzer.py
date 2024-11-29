from constants.error_messages import ErrorMessages
from constants.languages_grammer import PYTHON_LANGUAGE
from constants.languages_meta_data import LANGUAGE_META_DATA
from tree_sitter import Parser


def is_code_not_safe(language, code):
    if language == "PYTHON":
        includes, variables = analyze_python_code(code)

    if len(includes) == 0 and len(variables) == 0:  # type: ignore
        return False, None

    for imp in includes:  # type: ignore
        module = imp.split(".")[0]
        if module in LANGUAGE_META_DATA[language]["restricted_modules"]:
            return True, ErrorMessages.MODULE_NOT_ALLOWED.value

    # for var in variables:
    #     if var.split()[1] in LANGUAGE_META_DATA[language]["restricted_modules"]:
    #         return False, var.split()[1]

    return False, None


def check_python_import_as_stmt(statement):
    if "as" in statement:
        return statement.split(" as ")[0]
    return statement


def analyze_python_code(code):
    parser = Parser(PYTHON_LANGUAGE)
    tree = parser.parse(bytes(code, "utf8"))

    includes = []
    variables = []

    def traverse_tree(node):
        if node.type == "import_statement":
            module_node = node.child(1)
            module_name = code[module_node.start_byte : module_node.end_byte]
            includes.append(check_python_import_as_stmt(module_name))

        elif node.type == "import_from_statement":
            if len(node.children) >= 4:
                module_node, import_node = node.child(1), node.child(3)

                module_name = code[module_node.start_byte : module_node.end_byte]
                import_name = code[import_node.start_byte : import_node.end_byte]
                includes.append(f"{module_name}.{import_name}")
            else:
                print("Warning: Unexpected structure in 'from_import_statement'")

        # elif node.type == "assignment":
        #     variables.append(code[node.start_byte : node.end_byte])

        for child in node.children:
            traverse_tree(child)

    traverse_tree(tree.root_node)
    return includes, variables
