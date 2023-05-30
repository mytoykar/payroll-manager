from enum import Enum


class FastAPIErrorTypes(str, Enum):

    INVALID_DATA_TYPE = "type_error"
    MISSING_REQUIRED_FIELD = "value_error.missing"
    INVALID_VALUE = "value_error"
