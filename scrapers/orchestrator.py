import asyncio
import logging

from httpx import AsyncClient
from justjoinit.scraper import JustJoinItScraper


class Orchestrator:
    def __init__(self) -> None:
        logger = logging.getLogger(__name__)
        api_client = AsyncClient(base_url="http://localhost:8000/")  # load from .env
        self._tasks = [JustJoinItScraper(api_client, logger=logger)]

    async def _run_async(self) -> None:
        async with asyncio.TaskGroup() as tg:
            for task in self._tasks:
                tg.create_task(coro=task.run(), name=task.name)

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run_async())
