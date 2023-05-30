from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, condecimal


class CalculateSalaryRequest(BaseModel):
    basic_rate: Optional[Decimal] = None
    absent_day_count: Optional[condecimal(ge=Decimal(0.0))]
    work_day_count: Optional[condecimal(ge=Decimal(0.0))]
