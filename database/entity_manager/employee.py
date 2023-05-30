from sqlalchemy.orm import Session

from database.entity.employee import Employee
from utils.pagination import Filters, PaginationParams

filter_map = {"name": "name", "tin": "tin", "is_deleted": "is_deleted"}


def get_employee_by_id(db: Session, employee_id: int) -> Employee:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employees_by_filter(
    db: Session, filters: Filters, skip: int = 0, limit: int = 100
):
    translated_filters = {
        filter_map.get(f_name): f_value
        for f_name, f_value in filters.dict().items()
        if f_value is not None
    }
    return (
        db.query(Employee)
        .filter_by(**translated_filters)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_by_filter(db: Session, query=PaginationParams):
    filters = query.filters
    translated_filters = {
        filter_map.get(f_name): f_value
        for f_name, f_value in filters.dict().items()
        if f_value is not None
    }
    return (
        db.query(Employee).filter_by(**translated_filters).count(),
        db.query(Employee)
        .filter_by(**translated_filters)
        .offset((query.page_number - 1) * query.page_size)
        .limit(query.page_size)
        .all(),
    )


def create_employee(db: Session, entry):
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def edit_employee(db: Session, employee_id: int, update_set: dict):
    entry = db.query(Employee).filter(Employee.id == employee_id)
    entry.update(update_set)
    db.commit()
    refreshed = db.query(Employee).filter(Employee.id == employee_id).first()
    return refreshed
