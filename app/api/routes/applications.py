from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.application import PipelineEntry
from app.models.company import Target
from app.models.user import User
from app.schemas.application import (
    PipelineEntryCreate,
    PipelineEntryOut,
    PipelineEntryUpdate,
)

router = APIRouter(prefix="/pipeline", tags=["pipeline"])


@router.post("", response_model=PipelineEntryOut)
def create_pipeline_entry(
    payload: PipelineEntryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    target = (
        db.query(Target)
        .filter(Target.id == payload.target_id, Target.owner_id == current_user.id)
        .first()
    )
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    pipeline_entry = PipelineEntry(**payload.model_dump(), owner_id=current_user.id)
    db.add(pipeline_entry)
    db.commit()
    db.refresh(pipeline_entry)
    return pipeline_entry


@router.get("", response_model=list[PipelineEntryOut])
def list_pipeline_entries(
    stage: str = "",
    target_id: int = 0,
    search: str = "",
    follow_up_due: bool = False,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(PipelineEntry).filter(PipelineEntry.owner_id == current_user.id)

    if stage:
        query = query.filter(PipelineEntry.stage == stage)

    if target_id:
        query = query.filter(PipelineEntry.target_id == target_id)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            PipelineEntry.position_title.ilike(pattern)
            | PipelineEntry.source.ilike(pattern)
        )

    if follow_up_due:
        query = query.filter(
            PipelineEntry.follow_up_date.is_not(None),
            PipelineEntry.follow_up_date <= date.today(),
            PipelineEntry.stage.notin_(["offer", "closed"]),
        )

    return (
        query.order_by(PipelineEntry.created_at.desc()).offset(skip).limit(limit).all()
    )


@router.get("/{entry_id}", response_model=PipelineEntryOut)
def get_pipeline_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pipeline_entry = (
        db.query(PipelineEntry)
        .filter(
            PipelineEntry.id == entry_id,
            PipelineEntry.owner_id == current_user.id,
        )
        .first()
    )
    if not pipeline_entry:
        raise HTTPException(status_code=404, detail="Pipeline entry not found")
    return pipeline_entry


@router.put("/{entry_id}", response_model=PipelineEntryOut)
def update_pipeline_entry(
    entry_id: int,
    payload: PipelineEntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pipeline_entry = (
        db.query(PipelineEntry)
        .filter(
            PipelineEntry.id == entry_id,
            PipelineEntry.owner_id == current_user.id,
        )
        .first()
    )
    if not pipeline_entry:
        raise HTTPException(status_code=404, detail="Pipeline entry not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "target_id" in update_data:
        target = (
            db.query(Target)
            .filter(
                Target.id == update_data["target_id"],
                Target.owner_id == current_user.id,
            )
            .first()
        )
        if not target:
            raise HTTPException(status_code=404, detail="Target not found")

    for key, value in update_data.items():
        setattr(pipeline_entry, key, value)

    db.commit()
    db.refresh(pipeline_entry)
    return pipeline_entry


@router.delete("/{entry_id}")
def delete_pipeline_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pipeline_entry = (
        db.query(PipelineEntry)
        .filter(
            PipelineEntry.id == entry_id,
            PipelineEntry.owner_id == current_user.id,
        )
        .first()
    )
    if not pipeline_entry:
        raise HTTPException(status_code=404, detail="Pipeline entry not found")

    db.delete(pipeline_entry)
    db.commit()
    return {"message": "Pipeline entry deleted"}
