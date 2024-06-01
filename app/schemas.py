from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class JobExperienceBase(BaseModel):
    job_title: str
    company_name: str

class JobExperienceResponse(JobExperienceBase):
    id: int
    id_user: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SkillBase(BaseModel):
    skill: str

class SkillCreate(SkillBase):
    pass

class SkillUpdate(SkillBase):
    pass

class SkillResponse(SkillBase):
    id: int
    id_user: int
    updated_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserSave(UserBase):
    id: int
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None

    job_experiences: Optional[List[JobExperienceBase]] = []
    skills: Optional[List[SkillBase]] = []

class UserResponse(UserBase):
    id: int
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None
