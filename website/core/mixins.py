from sqlmodel import Field
from datetime import datetime


class BaseModelMixin:
    id: int | None = Field(default=None, primary_key=True)

    created_at: datetime | None = Field(default_factory=datetime.now)
    deleted_at: datetime | None = None
    updated_at: datetime | None = None
