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
    Technology,
)

from .utils import SortTypeQuery
from .schemas import CreatePostingSchema


async def create_posting(db: DbSession, payload: CreatePostingSchema) -> Posting:
    instance = Posting.model_validate(payload)

    pre_existing_posting = await db.exec(
        Select(Posting).where(Posting.source_id == instance.source_id)
    )

    if existing_instance := pre_existing_posting.unique().one_or_none():
        # log that model already exists
        return existing_instance

    salary_stmt = select(Salary).where(
        Salary.from_amount == payload.salary_from,
        Salary.to_amount == payload.salary_to,
        Salary.currency == payload.salary_currency,
    )

    if not (salary := await find_one_or_none(db, salary_stmt)):
        salary = Salary(
            from_amount=payload.salary_from,
            to_amount=payload.salary_to,
            currency=payload.salary_currency,
            employment_type=payload.employment_type,
        )

        db.add(salary)

    tech_instances = []
    for tech in payload.raw_technologies:
        tech_stmt = select(Technology).where(
            func.lower(Technology.name) == func.lower(tech.name),
        )

        if not (technology := await find_one_or_none(db, tech_stmt)):
            technology = Technology(name=tech.name)

            db.add(technology)

        tech_instances.append(technology)

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
    instance.technologies = tech_instances

    db.add(instance)
    await db.commit()
    await db.refresh(instance)

    return instance


async def _paginate_postings(
    db: DbSession, page: int, order: SortTypeQuery
) -> tuple[list[Posting], int]:
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

    count_stmt = Select(func.count(Posting.id))
    rows_amount = await db.exec(count_stmt)

    return [row[0] for row in res.unique().all()], rows_amount.scalar_one()


async def serve_templated_postings(
    db: DbSession,
    request: Request,
    page: int = Query(1, ge=1),
    sort: SortTypeQuery | None = SortTypeQuery.DESC,
) -> HTMLResponse:
    postings, postings_count = await _paginate_postings(db, page, sort)

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
                {
                    "name": "Most Recent",
                    "active": sort == SortTypeQuery.DESC,
                    "href": "/?sort=desc",
                },
                {
                    "name": "Least Recent",
                    "active": sort == SortTypeQuery.ASC,
                    "href": "/?sort=asc",
                },
            ],
            "postings_count": postings_count,
            "postings": postings,
        }

    return templates.TemplateResponse(request=request, name=name, context=context)
