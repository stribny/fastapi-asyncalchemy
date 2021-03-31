from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from fastapi_asyncalchemy.db.base import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True)
    population = Column(Integer)
