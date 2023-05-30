from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from controller.employee import router as employee_router
from database.entity.base_entity import setup_db_conn
from exception.error_handlers import (
    bad_request_exception_handler,
    request_param_exception_handler,
)
from exception.request_param_exception import RequestParamException

app = FastAPI()

app.include_router(employee_router)

app.add_exception_handler(
    RequestValidationError, bad_request_exception_handler
)
app.add_exception_handler(
    RequestParamException, request_param_exception_handler
)


@app.on_event("startup")
def on_startup():
    setup_db_conn()
