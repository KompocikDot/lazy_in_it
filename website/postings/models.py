from sqlmodel import SQLModel, Field, Relationship


from core.mixins import BaseModelMixin
from postings.schemas import BasePostingSchema


class PostingsTechnologiesLink(SQLModel, table=True):
    technology_id: int | None = Field(
        default=None, foreign_key="technology.id", primary_key=True
    )
    posting_id: int | None = Field(
        default=None, foreign_key="posting.id", primary_key=True
    )


class Posting(BaseModelMixin, BasePostingSchema, table=True):
    company_id: int | None = Field(default=None, foreign_key="company.id")
    company: "Company" = Relationship(
        back_populates="postings", sa_relationship_kwargs={"lazy": "joined"}
    )

    city_id: int | None = Field(default=None, foreign_key="city.id")
    city: "City" = Relationship(
        back_populates="postings", sa_relationship_kwargs={"lazy": "joined"}
    )

    salary_id: int | None = Field(default=None, foreign_key="salary.id")
    salary: "Salary" = Relationship(
        back_populates="postings", sa_relationship_kwargs={"lazy": "joined"}
    )

    technologies: list["Technology"] = Relationship(
        back_populates="postings",
        link_model=PostingsTechnologiesLink,
        sa_relationship_kwargs={"lazy": "joined"},
    )


class Company(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(unique=True)

    postings: list[Posting] = Relationship(back_populates="company")


class City(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(unique=True)

    postings: list[Posting] = Relationship(back_populates="city")


class Salary(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    amount: str = Field(unique=True)

    postings: list[Posting] = Relationship(back_populates="salary")


class Technology(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(unique=True)

    postings: list[Posting] = Relationship(
        back_populates="technologies", link_model=PostingsTechnologiesLink
    )
