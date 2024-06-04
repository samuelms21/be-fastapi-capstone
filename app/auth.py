from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
import app.helpers as helpers

import uuid

SECRET_KEY = "12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email)
    if not user or not helpers.verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=30)

    to_encode.update({"exp": expire, "sub": data.get("sub")})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(db: Session = Depends(), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token[1:-1], SECRET_KEY, algorithms=[ALGORITHM])
        
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = schemas.TokenData(email=email)
    except JWTError as e:
        # print(e)
        raise credentials_exception

    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
