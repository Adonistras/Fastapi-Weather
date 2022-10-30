import datetime
from passlib.hash import bcrypt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from core.db import get_session
from schemas import users
from models.users import User
from schemas.users import Token, CreateUser
from settings import settings
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/sign-in")


def get_current_user(token: str = Depends(oauth2_scheme)) -> users.User:
        return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hash_password: str) -> bool:
        return bcrypt.verify(plain_password, hash_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def create_token(cls, user: User) -> Token:
        user_data = users.User.from_orm(user)
        now = datetime.datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + datetime.timedelta(seconds=settings.jwt_expiration),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(payload, settings.jwt_secret, settings.jwt_algorithm)

        return Token(access_token=token)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise exceptions
        user_data = payload.get("user")
        user = users.User.parse_obj(user_data)
        if user is None:
            raise exceptions
        return user

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register(self, user_data: CreateUser) -> Token:
        user = User(email=user_data.email, name=user_data.name,
                    password_hash=self.hash_password(user_data.password))
        self.session.add(user)
        self.session.commit()
        return self.create_token(user)


    def authenticate(self, name,
                 password,) -> Token:
        exceptions = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"})
        user = self.session.query(User).filter(User.name == name).first()
        if not user:
            raise exceptions

        if not self.verify_password(password, user.password_hash):
            raise exceptions
        return self.create_token(user)

