import requests
from fastapi import HTTPException
from starlette import status
from models.cities import City
from models.weather import Weather
from settings import settings
from datetime import datetime


def update_weather(url: dict, city: City):
    Weather(city_id=city.id,
            temp=url['main']['temp'],
            wind=url['wind']['speed'],
            pressure=url['main']['pressure'],
            clouds=url['weather'][0]['description'],
            created=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            icon=settings.api_icon.format(url['weather'][0]['icon']))


def validate_weather(city: str):
    exceptions = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                               detail="Invalid city name")
    city = city.lower()
    url = requests.get(settings.api_url.format(city)).json()
    if url['cod'] == 200:
        return url
    else:
        raise exceptions

