from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.application import PipelineEntry
from app.models.note import ActivityLog
from app.models.user import User
from app.schemas.note import ActivityLogCreate, ActivityLogOut, ActivityLogUpdate

router = APIRouter(prefix="/activity", tags=["activity"])


@router.post("", response_model=ActivityLogOut)
def create_activity_log(
    payload: ActivityLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pipeline_entry = (
        db.query(PipelineEntry)
        .filter(
            PipelineEntry.id == payload.pipeline_entry_id,
            PipelineEntry.owner_id == current_user.id,
        )
        .first()
    )
    if not pipeline_entry:
        raise HTTPException(status_code=404, detail="Pipeline entry not found")

    activity_log = ActivityLog(
        body=payload.body,
        pipeline_entry_id=payload.pipeline_entry_id,
        owner_id=current_user.id,
    )
    db.add(activity_log)
    db.commit()
    db.refresh(activity_log)
    return activity_log


@router.get("", response_model=list[ActivityLogOut])
def list_activity_logs(
    pipeline_entry_id: int = 0,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(ActivityLog).filter(ActivityLog.owner_id == current_user.id)

    if pipeline_entry_id:
        query = query.filter(ActivityLog.pipeline_entry_id == pipeline_entry_id)

    return query.order_by(ActivityLog.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{activity_id}", response_model=ActivityLogOut)
def get_activity_log(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activity_log = (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id, ActivityLog.owner_id == current_user.id)
        .first()
    )
    if not activity_log:
        raise HTTPException(status_code=404, detail="Activity log not found")
    return activity_log


@router.put("/{activity_id}", response_model=ActivityLogOut)
def update_activity_log(
    activity_id: int,
    payload: ActivityLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activity_log = (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id, ActivityLog.owner_id == current_user.id)
        .first()
    )
    if not activity_log:
        raise HTTPException(status_code=404, detail="Activity log not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(activity_log, key, value)

    db.commit()
    db.refresh(activity_log)
    return activity_log


@router.delete("/{activity_id}")
def delete_activity_log(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    activity_log = (
        db.query(ActivityLog)
        .filter(ActivityLog.id == activity_id, ActivityLog.owner_id == current_user.id)
        .first()
    )
    if not activity_log:
        raise HTTPException(status_code=404, detail="Activity log not found")

    db.delete(activity_log)
    db.commit()
    return {"message": "Activity log deleted"}
