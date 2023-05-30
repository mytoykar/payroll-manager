from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import condecimal, root_validator

from constants.enum.employee_types import EmployeeTypes
from database.entity.employee import EmployeeSchema
from exception.error_codes import ErrorCodes
from exception.request_param_exception import RequestParamException


class EmployeeEditRequest(EmployeeSchema):
    name: Optional[str]
    tin: Optional[str]
    birthdate: Optional[date]
    basic_rate: Optional[condecimal(ge=Decimal(0.0), decimal_places=2)]
    employee_type: Optional[EmployeeTypes]
    is_deleted: Optional[bool]

    @root_validator(pre=True)
    def validate_update_content(cls, values):
        if not values:
            raise RequestParamException(
                field="content",
                message="No updates to be made.",
                code=ErrorCodes.REQUIRED_CONTENT_MISSING.name,
            )

        return values
