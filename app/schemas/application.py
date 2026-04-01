from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PipelineStage(str, Enum):
    saved = "saved"
    outreach = "outreach"
    applied = "applied"
    assessment = "assessment"
    screen = "screen"
    interview = "interview"
    final_round = "final_round"
    offer = "offer"
    closed = "closed"


class PipelineEntryCreate(BaseModel):
    position_title: str
    stage: PipelineStage = PipelineStage.saved
    source: Optional[str] = None
    listing_url: Optional[str] = None
    applied_date: Optional[date] = None
    follow_up_date: Optional[date] = None
    compensation_min: Optional[int] = None
    compensation_max: Optional[int] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    target_id: int


class PipelineEntryUpdate(BaseModel):
    position_title: Optional[str] = None
    stage: Optional[PipelineStage] = None
    source: Optional[str] = None
    listing_url: Optional[str] = None
    applied_date: Optional[date] = None
    follow_up_date: Optional[date] = None
    compensation_min: Optional[int] = None
    compensation_max: Optional[int] = None
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    target_id: Optional[int] = None


class PipelineEntryOut(BaseModel):
    id: int
    position_title: str
    stage: PipelineStage
    source: Optional[str] = None
    listing_url: Optional[str] = None
    applied_date: Optional[date] = None
    follow_up_date: Optional[date] = None
    compensation_min: Optional[int] = None
    compensation_max: Optional[int] = None
    priority: Optional[int] = None
    target_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
