from typing import Optional

from database.entity.employee import EmployeeSchema


class EmployeeUpdateRequest(EmployeeSchema):
    is_deleted: Optional[bool]
