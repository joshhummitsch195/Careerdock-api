from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl


class PersonCreate(BaseModel):
    full_name: str
    title: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin_url: Optional[HttpUrl] = None
    relationship_notes: Optional[str] = None
    target_id: int


class PersonUpdate(BaseModel):
    full_name: Optional[str] = None
    title: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin_url: Optional[HttpUrl] = None
    relationship_notes: Optional[str] = None
    target_id: Optional[int] = None


class PersonOut(BaseModel):
    id: int
    full_name: str
    title: Optional[str] = None
    email: Optional[EmailStr] = None
    linkedin_url: Optional[str] = None
    relationship_notes: Optional[str] = None
    target_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
