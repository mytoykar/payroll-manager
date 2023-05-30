import copy
from unittest.mock import ANY

import pytest
from fastapi.testclient import TestClient

from main import app
from tests.test_factory import EMPLOYEE_ONE, EMPLOYEE_TWO

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_edited_employee(override_db):
    client.post("/api/employee/", json=EMPLOYEE_ONE)
    client.post("/api/employee/", json=EMPLOYEE_TWO)
    delete_request = {
        "is_deleted": True,
    }
    client.patch("/api/employee/1", json=delete_request)


def test_view_one_employee_deleted(setup_edited_employee):
    resp = client.get("/api/employee/1")
    json_resp = resp.json()
    assert json_resp == {
        "name": "name_test",
        "tin": "tin_test",
        "birthdate": "2020-01-20",
        "basic_rate": 100.0,
        "employee_type": "REGULAR",
        "id": 1,
        "created_at": ANY,
        "updated_at": ANY,
        "is_deleted": True,
    }


def test_view_employees_filtered_paginated(setup_edited_employee):
    employee_three = copy.deepcopy(EMPLOYEE_ONE)
    employee_three["name"] = "Third employee"
    client.post("/api/employee/", json=employee_three)
    page_size = 5
    page_number = 1
    resp = client.get(
        "/api/employee/",
        params={"page_size": page_size, "page_number": page_number},
    )
    json_resp = resp.json()
    assert json_resp == {
        "employees": [
            {
                "name": "name_test",
                "tin": "tin_test",
                "birthdate": "2020-01-20",
                "basic_rate": 500.0,
                "employee_type": "CONTRACTUAL",
                "id": 2,
                "created_at": ANY,
                "updated_at": ANY,
                "is_deleted": False,
            },
            {
                "name": "Third employee",
                "tin": "tin_test",
                "birthdate": "2020-01-20",
                "basic_rate": 100.0,
                "employee_type": "REGULAR",
                "id": 3,
                "created_at": ANY,
                "updated_at": ANY,
                "is_deleted": False,
            },
        ],
        "pagination": {
            "current_page": page_number,
            "current_page_records": 2,
            "records_per_page": page_size,
            "total_records": 2,
        },
    }


def test_view_employees_with_deleted_paginated(setup_edited_employee):
    page_size = 5
    page_number = 1
    resp_deleted = client.get(
        "/api/employee/",
        params={
            "page_size": page_size,
            "page_number": page_number,
            "is_deleted": True,
        },
    )
    json_resp_deleted = resp_deleted.json()
    assert json_resp_deleted == {
        "employees": [
            {
                "name": "name_test",
                "tin": "tin_test",
                "birthdate": "2020-01-20",
                "basic_rate": 100.0,
                "employee_type": "REGULAR",
                "id": 1,
                "created_at": ANY,
                "updated_at": ANY,
                "is_deleted": True,
            }
        ],
        "pagination": {
            "current_page": page_number,
            "current_page_records": 1,
            "records_per_page": page_size,
            "total_records": 1,
        },
    }
