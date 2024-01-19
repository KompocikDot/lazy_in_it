from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import SQLModel, Field, DateTime

from core.utils import CIStrEnum

from enum import auto


class Experience(CIStrEnum):
    INTERN = auto()
    JUNIOR = auto()
    MEDIOR = auto()
    SENIOR = auto()
    LEAD = auto()


class TypeOfWork(CIStrEnum):
    INTERNSHIP = auto()
    PART_TIME = auto()
    FULL_TIME = auto()
    FREELANCE = auto()


class EmploymentType(CIStrEnum):
    B2B = auto()
    PERMANENT = auto()
    INTERNSHIP = auto()
    TASK_SPECIFIC_CONTRACT = auto()
    MANDATE_CONTRACT = auto()


class WorkMode(CIStrEnum):
    REMOTE = auto()
    HYBRID = auto()
    OFFICE = auto()


class Currency(CIStrEnum):
    EUR = auto()
    GBP = auto()
    USD = auto()
    CAD = auto()
    CNY = auto()
    JPY = auto()
    PLN = auto()


class BaseCompanySchema(SQLModel):
    id: int
    name: str = Field(unique=True)


class BaseCitySchema(SQLModel):
    id: int
    name: str = Field(unique=True)


class BaseSalarySchema(SQLModel):
    id: int
    amount: str = Field(unique=True)
    currency: Currency


class BaseTechnologySchema(SQLModel):
    id: int
    name: str = Field(unique=True)


class BasePostingSchema(SQLModel):
    model_config = ConfigDict(validation_error_cause=True)

    job_title: str
    experience: Experience
    type_of_work: TypeOfWork
    employment_type: EmploymentType
    work_mode: WorkMode

    originally_published_at: datetime = Field(sa_type=DateTime(timezone=True))

    posting_url: str
    posting_photo: str | None


class CreatePostingSchema(BasePostingSchema):
    company_name: str
    city_name: str
    salary_amount: str
    salary_currency: Currency


class PostingSchema(BasePostingSchema):
    id: int
    company: BaseCompanySchema
    salary: BaseSalarySchema
    city: BaseCitySchema
    # technologies: list[BaseTechnologySchema]
