from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.templating import Jinja2Templates
from schemas.users import Token, CreateUser, User
from services.user_service import AuthService, get_current_user


router = APIRouter(prefix='/auth')
templates = Jinja2Templates(directory='templates')


"""Authorization's endpoints"""
@router.post('/sign-up', response_model=Token)
def sign_up(user_data: CreateUser, service: AuthService = Depends()):
    return service.register(user_data)


@router.post('/sign-in', response_model=Token)
def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), service: AuthService = Depends()):
    return service.authenticate(form_data.username, form_data.password)


@router.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user

