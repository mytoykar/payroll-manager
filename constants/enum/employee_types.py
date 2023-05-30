from enum import Enum


class EmployeeTypes(str, Enum):
    REGULAR = "REGULAR"
    CONTRACTUAL = "CONTRACTUAL"
