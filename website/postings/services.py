from sqlalchemy import func
from sqlmodel import select
from sqlmodel.sql.expression import Select, asc, desc
from fastapi.responses import HTMLResponse
from fastapi import Request, Query

from core.templates import templates
from core.db_funcs import find_one_or_none
from core.deps import DbSession
from core.settings import get_settings
from .models import (
    Salary,
    Company,
    City,
    Posting,
)

from .utils import SortTypeQuery
from .schemas import CreatePostingSchema


async def create_posting(db: DbSession, payload: CreatePostingSchema) -> Posting:
    print("data", type(payload), payload.experience, payload.work_mode)
    instance = Posting.model_validate(payload)

    salary_stmt = select(Salary).where(
        Salary.amount == payload.salary_amount,
        Salary.currency == payload.salary_currency,
    )
    if not (salary := await find_one_or_none(db, salary_stmt)):
        salary = Salary(amount=payload.salary_amount, currency=payload.salary_currency)
        db.add(salary)

    city_stmt = select(City).where(
        func.lower(City.name) == func.lower(payload.city_name)
    )
    if not (city := await find_one_or_none(db, city_stmt)):
        city = City(name=payload.city_name)
        db.add(city)

    company_stmt = select(Company).where(
        func.lower(Company.name) == func.lower(payload.company_name)
    )
    if not (company := await find_one_or_none(db, company_stmt)):
        company = Company(name=payload.company_name)
        db.add(company)

    await db.commit()

    instance.company = company
    instance.salary = salary
    instance.city = city

    db.add(instance)
    await db.commit()
    await db.refresh(instance)

    return instance


async def _paginate_postings(
    db: DbSession, page: int, order: SortTypeQuery
) -> list[Posting]:
    limit = get_settings().PAGINATION_LIMIT
    offset = (page - 1) * get_settings().PAGINATION_LIMIT

    if order == SortTypeQuery.DESC:
        order_func = desc
    else:
        order_func = asc

    stmt = (
        Select(Posting)
        .order_by(order_func(Posting.originally_published_at))
        .offset(offset)
        .limit(limit)
    )
    res = await db.exec(stmt)

    return [row[0] for row in res.unique().all()]


async def serve_templated_postings(
    db: DbSession,
    request: Request,
    page: int = Query(1, ge=1),
    sort: SortTypeQuery | None = SortTypeQuery.DESC,
) -> HTMLResponse:
    postings = await _paginate_postings(db, page, sort)

    if page and page > 1:
        name = "postings.j2"
        context = {
            "postings": postings,
            "page": page,
            "sort": sort,
        }

    else:
        name = "index.j2"
        context = {
            "page": 1,
            "sort": sort,
            "sort_options": [
                {"name": "Most Recent", "active": True, "href": "/?sort=desc"},
                {"name": "Least Recent", "active": False, "href": "/?sort=asc"},
            ],
            "postings_count": 4,
            "postings": postings,
        }

    return templates.TemplateResponse(request=request, name=name, context=context)
