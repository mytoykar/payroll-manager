from decimal import Decimal

from service.object_class.employee import EmployeeObj


class ContractualEmployee(EmployeeObj):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def calculate_salary(self):
        work_day_count = Decimal(
            str(self.employee_details.get("work_day_count", 0))
        )
        basic_rate = Decimal(str(self.employee_details.get("basic_rate")))

        return basic_rate * work_day_count
