from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_asyncalchemy.models import *
from fastapi_asyncalchemy.exceptions import DuplicatedEntryError


async def get_biggest_cities(session: AsyncSession) -> list[City]:
    result = await session.execute(select(City).order_by(City.population.desc()).limit(20))
    return result.scalars().all()


async def add_city(session: AsyncSession, name: str, population: int):
    new_city = City(name=name, population=population)
    session.add(new_city)
    try:
        await session.commit()
        return new_city
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The city is already stored")
    