import requests
from fastapi import Depends
from sqlalchemy.orm import session, Session
from starlette.responses import JSONResponse
from core.celery import celery_app
from core.db import get_session
from models.cities import City
from models.users import User
from models.weather import Weather, Weather_Service
from services.utils import update_weather
from settings import settings, conf
from fastapi_mail import FastMail, MessageSchema, MessageType


@celery_app.task(name='Update_weather')
def update_every_hour_weather(session: session = Depends(get_session)):
    cities = session.query(City).all()
    if not cities:
        return
    for city in cities:
        url = settings.api_url.format(city.name)
        result = requests.get(url).json()
        update_weather(result, city)
    return 'Updated'


@celery_app.task(name='Send_mail_every_hour')
def send_mail_every_hour(session: session = Depends(get_session)):
    users_subscriptions = session.query(Weather_Service).filter_by(remind='1')
    if not users_subscriptions:
        return 'Users not found'
    users = [[user.user_id, user.city_id] for user in users_subscriptions]
    send_emails.delay(users)
    return 'Success'


@celery_app.task(name='Send_mail_every_three_hours')
def send_mail_three_hours(session: session = Depends(get_session)):
    users_subscriptions = session.query(Weather_Service).filter_by(remind='3')
    if not users_subscriptions:
        return 'Users not found'
    users = [[user.user_id, user.city_id] for user in users_subscriptions]
    send_emails.delay(users)
    return 'Success'


@celery_app.task(name='Send_mail_every_five_hours')
def send_mail_five_hours(session: session = Depends(get_session)):
    users_subscriptions = session.query(Weather_Service).filter_by(remind='5')
    if not users_subscriptions:
        return 'Users not found'
    users = [[user.user_id, user.city_id] for user in users_subscriptions]
    send_emails.delay(users)
    return 'Success'


@celery_app.task('Send emails')
def send_emails(users: list, session: Session = Depends(get_session)):
    subject = 'The Weather Forecast For Tomorrow'
    for element in users:
        user = session.query(User).filter_by(id=element[0])
        city = session.query(City).filter_by(id=element[1])
        weather = session.query(Weather).filter_by(city=element[1])

        context = {
            'city': city.name,
            'icon': weather.icon,
            'wind': weather.wind,
            'temp': weather.temp,
            'pressure': weather.pressure,
            'clouds': weather.clouds,
        }

        message = MessageSchema(
            subject=subject,
            recipients=user.email,
            template_body=context,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)

        fm.send_message(message, template_name='body.html')
        return JSONResponse(status_code=200, content={"message": "email has been sent"})


