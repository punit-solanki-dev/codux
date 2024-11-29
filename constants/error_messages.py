from enum import Enum

class ErrorMessages(Enum):
    PROCESS_TIMEOUT = f"The code execution took longer than the allowed time limit. Please optimize your code or try again with a smaller input size."
    MODULE_NOT_ALLOWED = f"A module you have imported isn't available at the moment. It will be available soon."