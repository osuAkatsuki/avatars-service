from enum import Enum


class ErrorCode(str, Enum):
    INVALID_CONTENT = "invalid_content"
    INAPPROPRIATE_CONTENT = "inappropriate_content"

    SERVICE_UNAVAILABLE = "service_unavailable"


class Error:
    def __init__(self, user_feedback: str, code: ErrorCode):
        self.user_feedback = user_feedback
        self.code = code
