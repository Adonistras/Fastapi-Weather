from pydantic import BaseModel


class WeatherBase(BaseModel):
    temp: str
    wind: str
    pressure: str
    clouds: str
    created: str
    icon: str


class Weather(WeatherBase):

    class Config:
        orm_mode = True

