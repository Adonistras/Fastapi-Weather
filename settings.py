from fastapi_mail import ConnectionConfig
from pydantic import BaseSettings
import os
from dotenv import load_dotenv



class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    db_url: str = "postgresql://postgres:filippos3dg@localhost/weather_api"
    api_key: str = "2f89537362ba16bcc59d3a1ec2303f03"
    api_url: str = "https://api.openweathermap.org/data/2.5/weather?&units=metric&q={}&appid=" + api_key
    api_icon: str = "https://openweathermap.org/img/w/{}.png"
    jwt_algorithm: str = "HS256"
    jwt_expiration: int = 3600
    jwt_secret: str
    broker: str = "amqp://user:bitnami@localhost:5672//"


load_dotenv()
"""Email config"""
conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM=os.environ.get('MAIL_FROM'),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

settings = Settings(
    _env_file='.env',
    _env_file_encoding='UTF-8',
)