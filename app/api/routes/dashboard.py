from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.application import PipelineEntry
from app.models.company import Target
from app.models.contact import Person
from app.models.note import ActivityLog
from app.models.user import User

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/overview")
def get_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pipeline_query = db.query(PipelineEntry).filter(
        PipelineEntry.owner_id == current_user.id
    )
    stage_counts = {
        stage: count
        for stage, count in (
            pipeline_query.with_entities(
                PipelineEntry.stage,
                func.count(PipelineEntry.id),
            )
            .group_by(PipelineEntry.stage)
            .all()
        )
    }

    follow_up_due_count = pipeline_query.filter(
        PipelineEntry.follow_up_date.is_not(None),
        PipelineEntry.follow_up_date <= date.today(),
        PipelineEntry.stage.notin_(["offer", "closed"]),
    ).count()

    return {
        "total_targets": db.query(Target).filter(Target.owner_id == current_user.id).count(),
        "total_pipeline_entries": pipeline_query.count(),
        "total_people": db.query(Person).filter(Person.owner_id == current_user.id).count(),
        "total_activity_logs": db.query(ActivityLog)
        .filter(ActivityLog.owner_id == current_user.id)
        .count(),
        "follow_up_due": follow_up_due_count,
        "stage_breakdown": stage_counts,
    }
