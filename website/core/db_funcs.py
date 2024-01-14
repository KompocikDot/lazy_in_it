from sqlmodel.sql.expression import SelectOfScalar

from core.deps import DbSession


async def find_one_or_none(db: DbSession, query: SelectOfScalar):
    res = await db.exec(query)
    return res.one_or_none()
