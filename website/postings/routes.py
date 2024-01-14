from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse

from core.deps import DbSession
from core.templates import templates
from postings import services
from postings.schemas import CreatePostingSchema, PostingSchema
from postings.utils import SortTypeQuery

router = APIRouter(tags=["postings"])


@router.get("/")
async def index(
    db: DbSession,
    request: Request,
    page: int = Query(1, ge=1),
    sort: SortTypeQuery | None = SortTypeQuery.DESC,
) -> HTMLResponse:
    postings = await services.paginate_postings(db, page, sort)

    if page and page > 1:
        name = "postings.j2"
        context = {"postings": postings}

    else:
        name = "index.j2"
        context = {
            "sort_options": [
                {"name": "Most Recent", "active": True, "href": "/?sort=desc"},
                {"name": "Least Recent", "active": False, "href": "/?sort=asc"},
            ],
            "postings_count": 4,
            "postings": postings,
        }

    return templates.TemplateResponse(request=request, name=name, context=context)


@router.post("/postings/", response_model=PostingSchema)
async def create_posting(db: DbSession, new_posting: CreatePostingSchema):
    return await services.create_posting(db, new_posting)
