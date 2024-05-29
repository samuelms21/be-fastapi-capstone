from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class BlacklistToken(Base):
    __tablename__ = "blacklist_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    blacklisted_on = Column(DateTime, default=datetime.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    location = Column(String, nullable=True)
    education = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    job_experiences = relationship("JobExperience", back_populates="user")
    skills = relationship("Skill", back_populates="user")


class JobExperience(Base):
    __tablename__ = "job_experiences"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="job_experiences")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="skills")
