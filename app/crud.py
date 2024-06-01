from fastapi import HTTPException
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


def save_user_info(db: Session, user: schemas.UserSave):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update user info
    db_user.full_name = user.full_name
    db_user.phone = user.phone
    db_user.location = user.location
    db_user.education = user.education

    # Update past job experience
    for job_exp in user.job_experiences:
        db_job_exp = db.query(models.JobExperience).filter(models.JobExperience.id_user == user.id).first()
        if db_job_exp:
            db_job_exp.company_name = job_exp.company_name
            db_job_exp.job_title = job_exp.job_title
        else:
            new_job_exp = models.JobExperience(
                id_user=user.id,
                job_title=job_exp.job_title,
                company_name=job_exp.company_name
            )
            db.add(new_job_exp)
    
    # Update Skills
    for skill in user.skills:
        db_skill = db.query(models.Skill)


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