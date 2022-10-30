import sqlalchemy
from core.db import Base


class User(Base):
    __tablename__ = "user"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String)