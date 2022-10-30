from typing import Dict
from datetime import datetime
from schemas.cities import CityWeather
from schemas.weather import WeatherBase
from services.utils import validate_weather
from settings import settings


def get_weather(city: str):
    value: Dict = {}
    weather = validate_weather(city)
    value[city] = {'time': datetime.now(), 'value': weather}
    return value


"""service for quick getting weather on the main page"""
def fast_weather(city: str) -> CityWeather:
    url = validate_weather(city)
    weather = WeatherBase(temp=url['main']['temp'],
                          wind=url['wind']['speed'],
                          pressure=url['main']['pressure'],
                          clouds=url['weather'][0]['description'],
                          created=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                          icon=settings.api_icon.format(url['weather'][0]['icon'])
                          )
    print(type(weather.created))
    value = CityWeather(name=city,
                        weather=weather)
    return value




