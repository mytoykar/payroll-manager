from constants.enum.employee_types import EmployeeTypes
from model.request.calculate_salary_request import CalculateSalaryRequest
from model.response.calculate_salary_response import CalculateSalaryResponse
from model.response.employee_response import EmployeeBaseModel
from service.object_class.contractual_employee import ContractualEmployee
from service.object_class.regular_employee import RegularEmployee

PROCESSOR_CLASS_MAP = {
    EmployeeTypes.REGULAR.name: RegularEmployee,
    EmployeeTypes.CONTRACTUAL.name: ContractualEmployee,
}


def calculate(request: CalculateSalaryRequest, employee_object):
    req_dict = request.dict(exclude_unset=True)
    existing_employee_details = employee_object.__dict__
    employee_id = existing_employee_details.get("id")
    saved_basic_rate = existing_employee_details.get("basic_rate")
    rate = req_dict.get("basic_rate") or saved_basic_rate

    calc_params = EmployeeBaseModel(**existing_employee_details).dict()
    calc_params.update(
        {
            "basic_rate": rate,
            "absent_day_count": req_dict.get("absent_day_count"),
            "work_day_count": req_dict.get("work_day_count"),
        }
    )

    employee_type = calc_params.get("employee_type")

    processor_class = PROCESSOR_CLASS_MAP.get(employee_type.name)
    processor = processor_class(**calc_params)
    computed_salary = processor.calculate_salary()
    return CalculateSalaryResponse(
        salary=computed_salary, employee_id=employee_id
    )
