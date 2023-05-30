import copy

from exception.error_codes import ErrorCodes
from model.request.employee_create_request import EmployeeCreateRequest

BASE_REQUEST = {
    "name": "name_test",
    "tin": "tin_test",
    "birthdate": "2020-01-20",
    "basic_rate": 100.00,
    "employee_type": "REGULAR",
}

EMPLOYEE_ONE = copy.deepcopy(BASE_REQUEST)
EMPLOYEE_TWO = {
    "name": "name_test",
    "tin": "tin_test",
    "birthdate": "2020-01-20",
    "basic_rate": 500.00,
    "employee_type": "CONTRACTUAL",
}


class TestDataFactory:
    def invalid_type_employee_create_request(self):
        # birthdate
        date_error_request = copy.deepcopy(BASE_REQUEST)
        date_error_request["birthdate"] = "2020-01-aa"
        date_error_response = {
            "message": "birthdate must be a valid date. Supported format: ISO 8601 (YYYY-MM-DD).",  # noqa: E501
            "code": ErrorCodes.INVALID_DATA_TYPE.name,
            "field": "birthdate",
        }

        # basic_rate
        decimal_error_request = copy.deepcopy(BASE_REQUEST)
        decimal_error_request["basic_rate"] = "A"
        decimal_error_response = {
            "message": "basic_rate must be a valid decimal.",
            "code": ErrorCodes.INVALID_DATA_TYPE.name,
            "field": "basic_rate",
        }

        # employee_type
        enum_error_request = copy.deepcopy(BASE_REQUEST)
        enum_error_request["employee_type"] = "ABSTRACT"
        enum_error_response = {
            "message": "ABSTRACT is not a valid Employee Type. Options are: [REGULAR, CONTRACTUAL].",  # noqa: E501
            "code": ErrorCodes.INVALID_OPTION.name,
            "field": "employee_type",
        }

        return [
            (date_error_request, date_error_response),
            (decimal_error_request, decimal_error_response),
            (enum_error_request, enum_error_response),
        ]

    def missing_required_employee_create_request(self):
        required_req_resp = []
        for (
            field_name,
            model_field,
        ) in EmployeeCreateRequest.__fields__.items():
            if model_field.required:
                removed_field_req = copy.deepcopy(BASE_REQUEST)
                removed_field_req.pop(field_name)
                required_req_resp.append(
                    (
                        removed_field_req,
                        {
                            "message": f"{field_name} is a required field.",
                            "code": ErrorCodes.REQUIRED_CONTENT_MISSING.name,
                            "field": f"{field_name}",
                        },
                    )
                )

        return required_req_resp
