import asyncio
import typer
from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
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
    city = await service.add_city(session, city.name, city.population)
    return city


if __name__ == "__main__":
    cli()
