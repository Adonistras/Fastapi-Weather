from enum import Enum
from core.db import Base
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType


class Weather(Base):
    __tablename__ = "weather"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    city_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('cities.id'))
    temp = sqlalchemy.Column(sqlalchemy.String(5))
    wind = sqlalchemy.Column(sqlalchemy.String(50))
    pressure = sqlalchemy.Column(sqlalchemy.String(50))
    clouds = sqlalchemy.Column(sqlalchemy.String(50))
    created = sqlalchemy.Column(sqlalchemy.DateTime)
    icon = sqlalchemy.Column(sqlalchemy.String(100))
    city = relationship('City', backref='weather', cascade="all, delete")


class NumRemind(Enum):
    none = '0'
    one_hour = '1'
    three_hours = '3'
    five_hours = '5'


class Weather_Service(Base):
    __tablename__ = "weather_service"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    remind = sqlalchemy.Column(ChoiceType(NumRemind), default=NumRemind.none)
    city_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('cities.id'))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'))
    city = relationship('City', backref='service')
    user = relationship('User', backref='service')

