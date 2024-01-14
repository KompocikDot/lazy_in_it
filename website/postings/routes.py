from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse


from core.templates import templates

router = APIRouter(tags=["postings"])


@router.get("/", response_class=HTMLResponse)
async def mainpage(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.j2",
        context={
            "postings": [
                {
                    "job_title": "Python developer with DevOps skillset",
                    "experience": "senior",
                    "technologies": [
                        "python",
                        "javascript",
                        "jenkins",
                        "aws",
                        "gcp",
                    ],
                    "city": "San Francisco",
                    "salary": {"currency": "EUR", "amount": "100"},
                    "company": "Apple Inc.",
                    "posting_url": "https://justjoinit.com/",
                },
                {
                    "job_title": "Python developer with DevOps skillset",
                    "experience": "senior",
                    "technologies": [
                        "python",
                        "javascript",
                        "jenkins",
                        "aws",
                        "gcp",
                    ],
                    "city": "San Francisco",
                    "salary": {"currency": "EUR", "amount": "100"},
                    "company": "Apple Inc.",
                },
                {
                    "job_title": "Python developer with DevOps skillset",
                    "experience": "senior",
                    "technologies": [
                        "python",
                        "javascript",
                        "jenkins",
                        "aws",
                        "gcp",
                    ],
                    "city": "San Francisco",
                    "salary": {"currency": "EUR", "amount": "100"},
                    "company": "Apple Inc.",
                },
                {
                    "job_title": "Python developer with DevOps skillset",
                    "experience": "senior",
                    "technologies": [
                        "python",
                        "javascript",
                        "jenkins",
                        "aws",
                        "gcp",
                    ],
                    "city": "San Francisco",
                    "salary": {"currency": "EUR", "amount": "100"},
                    "company": "Apple Inc.",
                },
            ]
        },
    )
