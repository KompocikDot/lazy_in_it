from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from enum import StrEnum, auto


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


class PostingsTechnologiesLink(SQLModel, table=True):
    technology_id: int | None = Field(
        default=None, foreign_key="technology.id", primary_key=True
    )
    posting_id: int | None = Field(
        default=None, foreign_key="posting.id", primary_key=True
    )


class Posting(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    job_title: str
    experience: Experience
    type_of_work: TypeOfWork
    employment_type: EmploymentType
    work_mode: WorkMode

    originally_published_at: datetime

    posting_url: str
    posting_photo: str | None

    company_id: int | None
    company: "Company" = Relationship(back_populates="postings")

    city_id: int | None
    city: "City" = Relationship(back_populates="postings")

    salary_id: int | None
    salary: "Salary" = Relationship(back_populates="postings")

    technologies: list["Technology"] = Relationship(
        back_populates="postings", link_model=PostingsTechnologiesLink
    )


class Company(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str

    postings: list[Posting] = Relationship(back_populates="team")


class City(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str

    postings: list[Posting] = Relationship(back_populates="city")


class Salary(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str

    postings: list[Posting] = Relationship(back_populates="salary")


class Technology(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str

    postings: list[Posting] = Relationship(
        back_populates="technologies", link_model=PostingsTechnologiesLink
    )
