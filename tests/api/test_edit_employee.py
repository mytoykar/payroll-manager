from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from freezegun import freeze_time

from main import app
from tests.test_factory import EMPLOYEE_ONE, EMPLOYEE_TWO

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_employee_entries(override_db):
    client.post("/api/employee/", json=EMPLOYEE_ONE)
    client.post("/api/employee/", json=EMPLOYEE_TWO)


@freeze_time("2023-03-03")
def test_edit_employee(setup_employee_entries):
    now = datetime.now()
    edit_request = {
        "name": "new name",  # from name_test
        "basic_rate": 125.00,  # from 100
        "employee_type": "REGULAR",  # same
        "is_deleted": False,  # same
    }
    resp = client.patch("/api/employee/1", json=edit_request)
    json_resp = resp.json()

    assert json_resp["updated_at"] == now.isoformat()
    for k, v in EMPLOYEE_ONE.items():
        if k in edit_request:
            assert json_resp[k] == edit_request[k]
        else:
            assert json_resp[k] == v
