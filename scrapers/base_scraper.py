from datetime import datetime
from logging import Logger
from typing import Protocol

from httpx import AsyncClient
from pydantic import BaseModel


class DbInput(BaseModel):
    company_name: str
    city_name: str
    salary_amount: str
    salary_currency: str
    salary_amount: str
    job_title: str

    experience: str
    type_of_work: str
    employment_type: str
    work_mode: str

    originally_published_at: datetime

    posting_url: str
    posting_photo: str


class BaseScraperMixin:
    BASE_URL: str

    name: str
    sleep_time_sec: int

    def __init__(self, api_client, logger: Logger) -> None:
        self.name = self.__class__.__name__
        self.client = AsyncClient(
            base_url=self.BASE_URL, headers={"Content-Type": "application/json"}
        )
        self.logger = logger

        self.retries = 5  # load from .env
        self.sleep_time_sec = 60  # load it from .env
        self._api_client: AsyncClient = api_client

    async def insert_to_db(self, data: list[DbInput]) -> None:
        retries = self.retries
        for obj in data:
            api_pings = 0
            while api_pings < retries:
                req = await self._api_client.post(
                    "/postings/", data=obj.model_dump_json()
                )
                if 200 <= req.status_code <= 299:
                    break
                api_pings += 1


class BaseScraper(Protocol):
    async def scrape(self) -> any:
        ...

    async def run(self):
        ...

    def format_json_to_db(self, data: any) -> list[DbInput]:
        ...


class Scraper(BaseScraperMixin, BaseScraper):
    ...
