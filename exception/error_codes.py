from enum import Enum


class ErrorCodes(Enum):
    INVALID_DATA_TYPE = "INVALID_DATA_TYPE"
    REQUIRED_CONTENT_MISSING = "REQUIRED_CONTENT_MISSING"
    INVALID_OPTION = "INVALID_OPTION"