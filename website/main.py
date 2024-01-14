from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from core.settings import get_settings
from core.db import engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield


if not get_settings().DEBUG:
    app = FastAPI(docs_url=None, lifespan=lifespan)
else:
    app = FastAPI(lifespan=lifespan)
