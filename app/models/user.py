from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    targets = relationship("Target", back_populates="owner", cascade="all, delete")
    pipeline_entries = relationship(
        "PipelineEntry", back_populates="owner", cascade="all, delete"
    )
    activity_logs = relationship(
        "ActivityLog", back_populates="owner", cascade="all, delete"
    )
    people = relationship("Person", back_populates="owner", cascade="all, delete")
