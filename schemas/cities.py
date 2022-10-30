from pydantic import BaseModel
from schemas.weather import WeatherBase


class CityBase(BaseModel):
    name: str


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityWeather(CityBase):
    weather: WeatherBase