from tree_sitter import Language, Parser
import tree_sitter_python as pylanguage
import tree_sitter_cpp as cpplanguage
import tree_sitter_c as clanguage
import tree_sitter_java as javalanguage

C_LANGUAGE = Language(clanguage.language())
CPP_LANGUAGE = Language(cpplanguage.language())
JAVA_LANGUAGE = Language(javalanguage.language())
PYTHON_LANGUAGE = Language(pylanguage.language())
