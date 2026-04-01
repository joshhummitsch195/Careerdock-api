from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.company import Target
from app.models.contact import Person
from app.models.user import User
from app.schemas.contact import PersonCreate, PersonOut, PersonUpdate

router = APIRouter(prefix="/people", tags=["people"])


@router.post("", response_model=PersonOut)
def create_person(
    payload: PersonCreate,
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

    person = Person(**payload.model_dump(mode="json"), owner_id=current_user.id)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@router.get("", response_model=list[PersonOut])
def list_people(
    target_id: int = 0,
    search: str = "",
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Person).filter(Person.owner_id == current_user.id)

    if target_id:
        query = query.filter(Person.target_id == target_id)

    if search:
        pattern = f"%{search}%"
        query = query.filter(Person.full_name.ilike(pattern) | Person.title.ilike(pattern))

    return query.order_by(Person.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{person_id}", response_model=PersonOut)
def get_person(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.owner_id == current_user.id)
        .first()
    )
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.put("/{person_id}", response_model=PersonOut)
def update_person(
    person_id: int,
    payload: PersonUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.owner_id == current_user.id)
        .first()
    )
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    update_data = payload.model_dump(exclude_unset=True, mode="json")
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
        setattr(person, key, value)

    db.commit()
    db.refresh(person)
    return person


@router.delete("/{person_id}")
def delete_person(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    person = (
        db.query(Person)
        .filter(Person.id == person_id, Person.owner_id == current_user.id)
        .first()
    )
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    db.delete(person)
    db.commit()
    return {"message": "Person deleted"}
