import sqlalchemy
from core.db import Base
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "cities"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    relationship('Weather', cascade="all, delete")

