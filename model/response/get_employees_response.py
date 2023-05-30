from typing import List, Optional

from pydantic import BaseModel

from model.response.employee_response import EmployeeBaseModel
from utils.pagination import PageInfo


class GetEmployeesBaseModel(BaseModel):
    employees: Optional[List[EmployeeBaseModel]]
    pagination: PageInfo
