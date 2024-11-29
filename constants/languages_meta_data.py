LANGUAGE_META_DATA = {
    "PYTHON": {
        "extension": ".py",
        "compilation_required": False,
        "execution_command": ["python"],
        "restricted_modules": ["os", "subprocess", "pathlib", "glob", "shutil", "sys", "builtins"],
    },
    "CPP": {
        "extension": ".cpp",
        "compilation_required": True,
        "execution_command": ["g++", "-o"],
    },
    "C": {
        "extension": ".c",
        "compilation_required": True,
        "execution_command": ["gcc", "-o"],
    },
    "JAVA": {
        "extension": ".java",
        "compilation_required": False,
        "execution_command": ["java"],
    },
}