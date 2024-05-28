from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    # id: int
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    education: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True