from datetime import datetime
from decimal import Decimal

from pydantic import root_validator

from database.entity.employee import EmployeeSchema
from utils.rounding import round_up_two_places


class EmployeeBaseModel(EmployeeSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def round_decimal(cls, values):
        for k, v in values.items():
            if isinstance(v, Decimal):
                values[k] = round_up_two_places(v)
        return values
