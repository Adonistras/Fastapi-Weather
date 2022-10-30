from fastapi import APIRouter
from api import city
from api import users
from api import weather
from api import main_page


routers = APIRouter()


routers.include_router(city.router)
routers.include_router(users.router)
routers.include_router(weather.router)
routers.include_router(main_page.router)