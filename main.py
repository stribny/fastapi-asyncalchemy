import asyncio
import typer
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from fastapi_asyncalchemy.exceptions import DuplicatedEntryError
from fastapi_asyncalchemy.db.base import init_models
from fastapi_asyncalchemy.db.base import get_session
from fastapi_asyncalchemy import service


app = FastAPI()
cli = typer.Typer()


class CitySchema(BaseModel):
    name: str
    population: int


@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")


@app.get("/cities/biggest", response_model=list[CitySchema])
async def get_biggest_cities(session: AsyncSession = Depends(get_session)):
    cities = await service.get_biggest_cities(session)
    return [CitySchema(name=c.name, population=c.population) for c in cities]


@app.post("/cities/")
async def add_city(city: CitySchema, session: AsyncSession = Depends(get_session)):
    city = service.add_city(session, city.name, city.population)
    try:
        await session.commit()
        return city
    except IntegrityError as ex:
        await session.rollback()
        raise DuplicatedEntryError("The city is already stored")


if __name__ == "__main__":
    cli()
