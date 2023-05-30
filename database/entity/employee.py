from datetime import date
from decimal import Decimal

from pydantic import BaseModel, condecimal, root_validator
from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, String

from constants.enum.employee_types import EmployeeTypes
from database.entity.base_entity import Base
from exception.error_codes import ErrorCodes
from exception.request_param_exception import RequestParamException


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    tin = Column(String, index=True)
    birthdate = Column(Date)
    basic_rate = Column(Float)
    employee_type = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, default=False)


# pydantic schemas
class EmployeeSchema(BaseModel):
    name: str
    tin: str
    birthdate: date
    basic_rate: condecimal(ge=Decimal(0.0), decimal_places=2)
    employee_type: EmployeeTypes

    @root_validator(pre=True)
    def validate_employee_type(cls, values):
        employee_type = values.get("employee_type")
        valid_type_options = [t.name for t in EmployeeTypes]
        if employee_type and employee_type not in valid_type_options:
            options = ", ".join(valid_type_options)
            raise RequestParamException(
                field="employee_type",
                message=f"{employee_type} is not a valid Employee Type. Options are: [{options}].",  # noqa: E501
                code=ErrorCodes.INVALID_OPTION.name,
            )
        return values
