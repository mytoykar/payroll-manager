from datetime import datetime

from fastapi.testclient import TestClient
from freezegun import freeze_time

from main import app
from tests.test_factory import EMPLOYEE_ONE, EMPLOYEE_TWO

client = TestClient(app)


@freeze_time("2023-03-01")
def test_create_employee(override_db):
    now = datetime.now()
    resp = client.post("/api/employee/", json=EMPLOYEE_ONE)

    assert resp.json() == {
        "name": "name_test",
        "tin": "tin_test",
        "birthdate": "2020-01-20",
        "basic_rate": 100.0,
        "employee_type": "REGULAR",
        "id": 1,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "is_deleted": False,
    }
    resp = client.post("/api/employee/", json=EMPLOYEE_TWO)

    assert resp.json() == {
        "name": "name_test",
        "tin": "tin_test",
        "birthdate": "2020-01-20",
        "basic_rate": 500.0,
        "employee_type": "CONTRACTUAL",
        "id": 2,
        "created_at": now.isoformat(),
        "updated_at": now.isoformat(),
        "is_deleted": False,
    }
