from decimal import Decimal

from pydantic import BaseModel, root_validator

from utils.rounding import round_up_two_places


class CalculateSalaryResponse(BaseModel):
    employee_id: int
    salary: Decimal

    @root_validator(pre=True)
    def round_decimal(cls, values):
        for k, v in values.items():
            if isinstance(v, Decimal):
                values[k] = round_up_two_places(v)
        return values
