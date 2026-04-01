from datetime import datetime

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class PipelineEntry(Base):
    __tablename__ = "pipeline_entries"

    id = Column(Integer, primary_key=True, index=True)
    position_title = Column(String, index=True, nullable=False)
    stage = Column(String, default="saved", nullable=False)
    source = Column(String, nullable=True)
    listing_url = Column(String, nullable=True)
    applied_date = Column(Date, nullable=True)
    follow_up_date = Column(Date, nullable=True)
    compensation_min = Column(Integer, nullable=True)
    compensation_max = Column(Integer, nullable=True)
    priority = Column(Integer, nullable=True)
    target_id = Column(Integer, ForeignKey("targets.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    target = relationship("Target", back_populates="pipeline_entries")
    owner = relationship("User", back_populates="pipeline_entries")
    activity_logs = relationship(
        "ActivityLog", back_populates="pipeline_entry", cascade="all, delete"
    )
