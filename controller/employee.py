from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.entity.base_entity import get_db_session
from model.request.calculate_salary_request import CalculateSalaryRequest
from model.request.employee_create_request import EmployeeCreateRequest
from model.request.employee_edit_request import EmployeeEditRequest
from model.response.calculate_salary_response import CalculateSalaryResponse
from model.response.employee_edit_response import EmployeeEditResponse
from model.response.employee_response import EmployeeBaseModel
from model.response.get_employees_response import GetEmployeesBaseModel
from service.employee import (
    calculate_employee_salary,
    create_employee,
    edit_employee,
    get_employee_by_employee_id,
    get_employee_list,
)
from utils.pagination import PaginationParams, pagination_params

router = APIRouter(prefix="/api/employee", tags=["Employees"])


@router.get("/{employee_id}", response_model=EmployeeBaseModel)
def get_employee_details_by_id(
    employee_id: int, db: Session = Depends(get_db_session)
):

    return get_employee_by_employee_id(db=db, employee_id=employee_id)


@router.get("/", response_model=GetEmployeesBaseModel)
def get_employees_paginated(
    query: Optional[PaginationParams] = Depends(pagination_params),
    db: Session = Depends(get_db_session),
):

    return get_employee_list(db=db, query=query)


@router.post("/", response_model=EmployeeBaseModel)
def add_employee(
    request: EmployeeCreateRequest, db: Session = Depends(get_db_session)
):
    return create_employee(db=db, request=request)


@router.patch("/{employee_id}", response_model=EmployeeEditResponse)
def edit_employee_by_id(
    employee_id: int,
    request: EmployeeEditRequest,
    db: Session = Depends(get_db_session),
):

    return edit_employee(db=db, employee_id=employee_id, request=request)


@router.put(
    "/{employee_id}/calculate-salary", response_model=CalculateSalaryResponse
)
def calculate_salary(
    employee_id: int,
    request: CalculateSalaryRequest,
    db: Session = Depends(get_db_session),
):

    return calculate_employee_salary(
        db=db, employee_id=employee_id, request=request
    )
