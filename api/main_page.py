from fastapi import Form, APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from starlette.templating import Jinja2Templates
from schemas.cities import CityWeather
from services.city import fast_weather


router = APIRouter()
templates = Jinja2Templates(directory='templates')


_cache = None

"""Main page"""
@router.get('/', response_class=HTMLResponse)
async def home(request: Request) -> Response:
    return templates.TemplateResponse(
        name='index.html',
        context={'request': request}
    )


"""Main page test post request"""
@router.post('/', response_model=CityWeather)
async def city_weather(request: Request, city: str = Form(...)):
    city = fast_weather(city)
    return templates.TemplateResponse(
        name='test.html',
        context={'request': request, 'city': city},
    )


@router.delete('/')
def delete_request():
    return HTMLResponse('')