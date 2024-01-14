from datetime import datetime
from enum import StrEnum, auto

from sqlmodel import SQLModel


class Experience(StrEnum):
    INTERN = auto()
    JUNIOR = auto()
    MEDIOR = auto()
    SENIOR = auto()
    LEAD = auto()


class TypeOfWork(StrEnum):
    INTERNSHIP = auto()
    PART_TIME = auto()
    FULL_TIME = auto()
    FREELANCE = auto()


class EmploymentType(StrEnum):
    B2B = auto()
    PERMANENT = auto()
    INTERNSHIP = auto()
    TASK_SPECIFIC_CONTRACT = auto()
    MANDATE_CONTRACT = auto()


class WorkMode(StrEnum):
    REMOTE = auto()
    HYBRID = auto()
    STATIONARY = auto()


class Currency(StrEnum):
    EUR = auto()
    GBP = auto()
    USD = auto()
    CAD = auto()
    CNY = auto()
    JPY = auto()
    PLN = auto()


class BasePostingSchema(SQLModel):
    job_title: str
    experience: Experience
    type_of_work: TypeOfWork
    employment_type: EmploymentType
    work_mode: WorkMode

    originally_published_at: datetime

    posting_url: str
    posting_photo: str | None


class CreatePostingSchema(BasePostingSchema):
    company_name: str
    city_name: str
    salary_amount: str
    salary_currency: Currency


class PostingSchema(BasePostingSchema):
    id: int
