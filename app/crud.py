from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas
from app.helpers import hash_password

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()

    # Re-fetch a database object & sync its state with the database
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def add_token_to_blacklist(db: Session, token: str) -> bool:
    db_token = models.BlacklistToken(token=token)
    db.add(db_token)
    try:
        db.commit()
        db.refresh(db_token)
        return True
    except IntegrityError:
        db.rollback()
        return False


def is_token_blacklisted(db: Session, token: str) -> bool:
    return db.query(models.BlacklistToken).filter_by(token=token).first() is not None