from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TargetCreate(BaseModel):
    name: str
    website: Optional[str] = None
    location: Optional[str] = None
    focus_area: Optional[str] = None


class TargetUpdate(BaseModel):
    name: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    focus_area: Optional[str] = None


class TargetOut(BaseModel):
    id: int
    name: str
    website: Optional[str] = None
    location: Optional[str] = None
    focus_area: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
