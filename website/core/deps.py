from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session

DbSession = Annotated[AsyncSession, Depends(get_session)]
