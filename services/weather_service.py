from datetime import datetime
import requests
from fastapi import Depends, HTTPException, Response
from starlette import status
from core.db import get_session
from sqlalchemy.orm import Session
from models.cities import City
from models.weather import Weather_Service, NumRemind, Weather
from settings import settings
from services.utils import update_weather


class WeatherService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def __create_weather__(self, url: dict, city: City):
        weather = Weather(city_id=city.id, temp=url['main']['temp'],
                          wind=url['wind']['speed'], pressure=url['main']['pressure'],
                          clouds=url['weather'][0]['description'], created=str(datetime.now()),
                          icon=settings.api_icon.format(url['weather'][0]['icon']))
        self.session.add(weather)
        self.session.commit()
        return weather


    async def create_service(self, item: str, remind: NumRemind, user_id: int
                       ):
        exceptions = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                   detail="Invalid city name")
        city = item.lower()
        url = requests.get(settings.api_url.format(city)).json()
        if url['cod'] == 200:
            city = self.session.query(City).filter_by(name=city).first()
            if city:
                update_weather(url, city)
                self.session.commit()
            else:
                city = City(name=city)
                self.session.add(city)
                self.session.commit()
                self.__create_weather__(url, city)
        else:
            raise exceptions
        forecast = Weather_Service(user_id=user_id, city_id=city.id, remind=remind)
        self.session.add(forecast)
        self.session.commit()
        return self.session.query(Weather_Service).get(forecast.id)


    def delete_service(self, service_id: int):
        service = self.session.query(Weather_Service).filter_by(id=service_id).first()
        self.session.delete(service)
        return Response(status_code=status.HTTP_204_NO_CONTENT)