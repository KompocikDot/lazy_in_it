from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from .settings import get_settings


engine = AsyncEngine(create_engine(get_settings().DB_URL, echo=True, future=True))

test_engine = create_async_engine(get_settings().DB_TEST_URL, future=True, echo=False)


async def get_session(test_session: bool = False) -> AsyncSession:
    async_session = sessionmaker(  # noqa
        test_engine if test_session else engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
