import copy

import pytest
from fastapi.testclient import TestClient

from main import app
from tests.test_factory import EMPLOYEE_ONE, EMPLOYEE_TWO

client = TestClient(app)

COMPUTE_BASE_REQUEST = {
    "basic_rate": 21333.00,
    "absent_day_count": 7.5,
    "work_day_count": 13.5,
}


@pytest.fixture(scope="function")
def setup_employee_entries(override_db):
    client.post("/api/employee/", json=EMPLOYEE_ONE)
    client.post("/api/employee/", json=EMPLOYEE_TWO)


def test_compute_salary_regular(setup_employee_entries):
    resp = client.put(
        "/api/employee/1/calculate-salary", json=COMPUTE_BASE_REQUEST
    )

    json_resp = resp.json()
    assert json_resp == {"employee_id": 1, "salary": 12373.14}


def test_compute_salary_contractual_no_override(setup_employee_entries):
    contractual_base_rate = copy.deepcopy(COMPUTE_BASE_REQUEST)
    contractual_base_rate.pop("basic_rate")
    resp = client.put(
        "/api/employee/2/calculate-salary", json=contractual_base_rate
    )

    json_resp = resp.json()
    assert json_resp == {"employee_id": 2, "salary": 6750.0}
