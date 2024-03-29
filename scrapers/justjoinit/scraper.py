import asyncio
import logging

from httpx import RequestError
from base_scraper import Scraper, DbInput, Technology


class JustJoinItScraper(Scraper):
    BASE_URL = "https://api.justjoin.it/v2/user-panel"

    async def scrape(self, page: int = 1) -> dict:
        while True:
            try:
                params = {
                    "page": page,
                    "sortBy": "published",
                    "orderBy": "DESC",
                    "perPage": 100,
                    "salaryCurrencies": "PLN",
                }

                req = await self.client.get(
                    "/offers", params=params, headers={"Version": "2"}
                )
                res = req.json()
                return res

            except RequestError as e:
                logging.exception(e)

    def format_json_to_db(self, data: any) -> list[DbInput]:
        raw_postings = data["data"]

        db_formatted_postings = []

        for posting in raw_postings:
            db_posting = DbInput(
                source_id=posting["slug"],
                city_name=posting["city"],
                posting_url=f"https://www.justjoin.it/offers/{posting['slug']}",
                posting_photo=posting["companyLogoThumbUrl"],
                job_title=posting["title"],
                work_mode=posting["workplaceType"],
                type_of_work=posting["workingTime"],
                experience=self.experience_to_db_format(posting["experienceLevel"]),
                company_name=posting["companyName"],
                # TODO: ONE POSTING CAN HAVE MULTIPLE TYPES AND SALARIES DEPENDING ON IT
                employment_type="b2b",
                # TODO: Change both below
                salary_from=posting["employmentTypes"][0].get("from", 0),
                salary_to=posting["employmentTypes"][0].get("to", 0),
                salary_currency="pln",
                originally_published_at=posting["publishedAt"],
                raw_technologies=[
                    Technology(name=tech_name)
                    for tech_name in posting["requiredSkills"]
                ],
            )

            db_formatted_postings.append(db_posting)

        return db_formatted_postings

    async def run(self) -> None:
        page = 1

        while True:
            scraped_data = await self.scrape(page=page)
            max_pages = scraped_data["meta"]["totalPages"]

            data_in_db_format = self.format_json_to_db(scraped_data)
            async with asyncio.TaskGroup() as internal_tg:
                tasks = []
                for index, data in enumerate(data_in_db_format):
                    task = internal_tg.create_task(
                        self.insert_to_db(data), name=f"{self.name} | {index}"
                    )
                    tasks.append(task)

            if max_pages == page:
                page = 1
                await asyncio.sleep(self.sleep_time_sec)

            else:
                page += 1
                await asyncio.sleep(self.sleep_time_between_pages)

    @staticmethod
    def experience_to_db_format(exp: str) -> str:
        match exp.lower():
            case "mid" | "medior":
                return "medior"
            case _:
                return exp
