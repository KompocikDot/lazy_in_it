from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse

from core.deps import DbSession
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
    return await services.serve_templated_postings(db, request, page, sort)


@router.post("/postings/", response_model=PostingSchema)
async def create_posting(db: DbSession, new_posting: CreatePostingSchema):
    return await services.create_posting(db, new_posting)
