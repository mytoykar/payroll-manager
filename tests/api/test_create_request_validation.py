import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from tests.test_factory import TestDataFactory

client = TestClient(app)

tdf = TestDataFactory()


@pytest.mark.parametrize(
    "request_response", tdf.invalid_type_employee_create_request()
)
def test_create_employee_with_invalid_data_type(request_response):
    request, expected_response = request_response

    resp = client.post("/api/employee/", json=request)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == expected_response


@pytest.mark.parametrize(
    "request_response", tdf.missing_required_employee_create_request()
)
def test_create_employee_with_missing_required_fields(request_response):
    request, expected_response = request_response

    resp = client.post("/api/employee/", json=request)

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp.json() == expected_response
