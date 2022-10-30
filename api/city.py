from fastapi import APIRouter
from starlette.templating import Jinja2Templates
from services.city import get_weather


router = APIRouter(prefix='/city')
templates = Jinja2Templates(directory="templates")


@router.get('/{city}')
def get_city_weather(city: str):
    weather = get_weather(city)
    return weather





