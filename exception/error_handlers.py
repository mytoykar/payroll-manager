from fastapi import status
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.logger import logger
from fastapi.responses import JSONResponse

from exception.error_codes import ErrorCodes
from exception.fastapi_error_types import FastAPIErrorTypes
from exception.request_param_exception import RequestParamException


async def bad_request_exception_handler(request, exc: RequestValidationError):
    """
    handles field validations before calling the pydantic BaseModel validators.
    """
    try:
        error = exc.errors()[0]
        msg = error["msg"]
        field = error["loc"][-1]
        error_type = error["type"]

        if error_type.split(".")[0] == FastAPIErrorTypes.INVALID_DATA_TYPE:
            data_type = error_type.split(".")[-1]
            data = {
                "field": field,
                "message": f"{field} must be a valid {data_type}.",
                "code": ErrorCodes.INVALID_DATA_TYPE.name,
            }

            if (
                data_type == "not_allowed"
                and error_type.split(".")[1] == "none"
            ):
                data = {
                    "field": field,
                    "message": f"{field} is a required field.",
                    "code": ErrorCodes.REQUIRED_CONTENT_MISSING.name,
                }

            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=data,
            )
        elif error_type == FastAPIErrorTypes.MISSING_REQUIRED_FIELD:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "field": field,
                    "message": f"{field} is a required field.",
                    "code": ErrorCodes.REQUIRED_CONTENT_MISSING.name,
                },
            )
        elif error_type == FastAPIErrorTypes.INVALID_VALUE:
            permitted = msg.split(":")[-1]
            value = msg.split(" ")[1]
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "field": field,
                    "message": f"{value} is not a valid "
                    f"{field} option:{permitted}",
                    "code": ErrorCodes.INVALID_OPTION.name,
                },
            )
        elif FastAPIErrorTypes.INVALID_VALUE in error_type:
            data_type = error_type.split(".")[-1]
            if data_type == "date":
                data_type += ". Supported format: ISO 8601 (YYYY-MM-DD)"
            elif data_type == "max_places":
                data_type = "decimal with 2 places."
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "field": field,
                    "message": f"{field} must be a valid {data_type}.",
                    "code": ErrorCodes.INVALID_DATA_TYPE.name,
                },
            )
        else:
            return await request_validation_exception_handler(request, exc)
    except Exception as e:
        logger.error(e)
        logger.error(e.__dict__)
        return await request_validation_exception_handler(request, exc)


async def request_param_exception_handler(request, exc: RequestParamException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "field": exc.field,
            "message": exc.message,
            "code": exc.code,
        },
    )
