from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ActivityLogCreate(BaseModel):
    body: str
    pipeline_entry_id: int


class ActivityLogUpdate(BaseModel):
    body: Optional[str] = None


class ActivityLogOut(BaseModel):
    id: int
    body: str
    pipeline_entry_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
