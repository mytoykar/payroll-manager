from fastapi import status


class RequestParamException(Exception):
    def __init__(
        self, field, message, code, status_code=status.HTTP_400_BAD_REQUEST
    ):
        self.field = field
        self.message = message
        self.code = code
        self.status_code = status_code
