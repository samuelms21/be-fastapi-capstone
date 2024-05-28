from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import crud, models, schemas
from .database import SessionLocal, engine
from .auth import authenticate_user, create_access_token, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}
        

@app.post("/users/register/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db=db, user=user)


# Tje response will be validated against the LoginResponse schema
@app.post("/users/login/", response_model=schemas.LoginResponse)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):

    # Depends(get_db) -> injects a database session, dependency injection
    # passes the database session and form data to authenticate user

    user = authenticate_user(db, form_data.username, form_data.password)

    # If not authenticated, return error
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",

            # to indicate the request requires HTTP authentication
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # If authenticated, create token
    access_token_expires = timedelta(minutes=30) # set token expiration time
    access_token = create_access_token(
        # generate a JWT Token
        # "sub" means subject, which is the user email
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "user": user}