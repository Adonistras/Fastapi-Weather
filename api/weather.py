from fastapi import APIRouter, Depends
from schemas.users import User
from models.weather import NumRemind
from services.user_service import get_current_user
from services.weather_service import WeatherService


router = APIRouter(prefix='/weather')


@router.post('/create')
async def create_service(city: str,
                   nums: NumRemind,
                       user: User = Depends(get_current_user),
                       service: WeatherService = Depends()):

    return await service.create_service(item=city, remind=nums, user_id=user.id)


@router.delete('/delete')
async def delete_service(service_id: int, user: User = Depends(get_current_user), service: WeatherService = Depends()):
    return await service.delete_service(service_id=service_id)