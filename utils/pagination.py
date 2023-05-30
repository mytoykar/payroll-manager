from typing import Optional

from pydantic import BaseModel


class Filters(BaseModel):
    employee_id: Optional[int] = None
    tin: Optional[str] = None
    name: Optional[str] = ""
    is_deleted: Optional[bool] = False


class PaginationParams(BaseModel):
    page_size: Optional[int] = 100
    page_number: Optional[int] = 1
    filters: Optional[Filters] = None

    class Config:
        anystr_strip_whitespace = True


async def pagination_params(
    page_size: int = 100,
    page_number: int = 1,
    employee_id: Optional[int] = None,
    name: Optional[str] = None,
    tin: Optional[str] = None,
    is_deleted: Optional[bool] = False,
):

    filters = Filters(
        employee_id=employee_id,
        name=name,
        tin=tin,
        is_deleted=is_deleted,
    )

    return PaginationParams(
        page_size=page_size,
        page_number=page_number,
        filters=filters,
    )


class PageInfo(BaseModel):
    current_page: int
    current_page_records: int
    records_per_page: int
    total_records: int
