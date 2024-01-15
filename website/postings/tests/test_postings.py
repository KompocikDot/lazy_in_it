import pytest
from httpx import AsyncClient

from main import app
from core.db import get_session, get_test_session

app.dependency_overrides[get_session] = get_test_session

test_client = AsyncClient(app=app, base_url="http://localhost:8000/")


@pytest.mark.asyncio
async def test_create_posting_with_non_existing_relations():
    payload = {
        "job_title": "Python Junior",
        "experience": "Junior",
        "type_of_work": "part_time",
        "employment_type": "b2b",
        "work_mode": "hybrid",
        "originally_published_at": "2024-01-14T19:24:44.586",
        "posting_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "posting_photo": "http://tinyurl.com/5n8bk5tv",
        "company_name": "My future employeer :)",
        "city_name": "Wrocław",
        "salary_amount": "2500",
        "salary_currency": "pln",
    }

    res = await test_client.post("/postings/", json=payload)

    expected = {
        "job_title": "Python Junior",
        "experience": "junior",
        "type_of_work": "part_time",
        "employment_type": "b2b",
        "work_mode": "hybrid",
        "originally_published_at": "2024-01-14T19:24:44.586000",
        "posting_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "posting_photo": "http://tinyurl.com/5n8bk5tv",
        "company": {
            "name": "My future employeer :)",
        },
        "salary": {
            "amount": "2500",
            "currency": "pln",
        },
        "city": {
            "name": "Wrocław",
        },
    }

    data = res.json()

    # removing all ids
    data.pop("id")
    data["company"].pop("id")
    data["salary"].pop("id")
    data["city"].pop("id")

    assert data == expected, (res.status_code, data)
