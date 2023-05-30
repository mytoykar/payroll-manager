from decimal import Decimal

from constants.common import TAX_PERCENTAGE, WORKING_DAYS_MONTHLY
from service.object_class.employee import EmployeeObj


class RegularEmployee(EmployeeObj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def calculate_salary(self):
        absent_day_count = Decimal(
            str(self.employee_details.get("absent_day_count", 0))
        )
        basic_rate = Decimal(str(self.employee_details.get("basic_rate")))
        tax_percentage = Decimal(str(TAX_PERCENTAGE))
        days_per_month = Decimal(str(WORKING_DAYS_MONTHLY))

        return (
            basic_rate
            * (days_per_month - absent_day_count)
            / (days_per_month)
            * (1 - tax_percentage)
        )
