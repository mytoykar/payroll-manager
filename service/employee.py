from datetime import datetime

from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from database.entity.employee import Employee
from database.entity_manager import employee as employee_em
from model.request.employee_create_request import EmployeeCreateRequest
from model.request.employee_edit_request import EmployeeEditRequest
from model.response.get_employees_response import GetEmployeesBaseModel
from service import salary_calculator
from utils.pagination import PageInfo, PaginationParams


def get_employee_by_employee_id(db: Session, employee_id: int):
    existing_employee = employee_em.get_employee_by_id(
        db, employee_id=employee_id
    )
    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with id: {employee_id} does not exist.",
        )
    return existing_employee


def get_employee_list(db: Session, query: PaginationParams):
    total_records, employees = employee_em.get_by_filter(db, query)

    pagination = PageInfo(
        current_page=query.page_number,
        current_page_records=len(employees),
        records_per_page=query.page_size,
        total_records=total_records,
    )

    return GetEmployeesBaseModel(employees=employees, pagination=pagination)


def create_employee(db: Session, request: EmployeeCreateRequest):
    now = datetime.now()
    entry = Employee(
        name=request.name,
        tin=request.tin,
        birthdate=request.birthdate,
        basic_rate=request.basic_rate,
        employee_type=request.employee_type,
        created_at=now,
        updated_at=now,
    )

    return employee_em.create_employee(db=db, entry=entry)


def edit_employee(db: Session, employee_id: int, request: EmployeeEditRequest):
    now = datetime.now()
    update_set = request.dict(exclude_unset=True)
    update_set.update({"updated_at": now})

    return employee_em.edit_employee(
        db=db, employee_id=employee_id, update_set=update_set
    )


def calculate_employee_salary(db, employee_id, request):
    existing_employee = employee_em.get_employee_by_id(
        db, employee_id=employee_id
    )
    if not existing_employee:
        raise HTTPException(
            status_code=404,
            detail=f"Employee with id: {employee_id} does not exist.",
        )

    return salary_calculator.calculate(request, existing_employee)
