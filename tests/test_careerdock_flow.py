from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_careerdock.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)



def get_token():
    client.post(
        "/auth/register",
        json={
            "email": "careerdock@example.com",
            "full_name": "Career Dock",
            "password": "123456",
        },
    )
    response = client.post(
        "/auth/login",
        data={"username": "careerdock@example.com", "password": "123456"},
    )
    return response.json()["access_token"]



def test_careerdock_flow():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    target_response = client.post(
        "/targets",
        json={
            "name": "OpenAI",
            "website": "https://openai.com",
            "location": "Remote",
            "focus_area": "AI tools and products",
        },
        headers=headers,
    )
    assert target_response.status_code == 200
    target_id = target_response.json()["id"]

    pipeline_response = client.post(
        "/pipeline",
        json={
            "position_title": "Software Engineering Intern",
            "stage": "applied",
            "source": "LinkedIn",
            "priority": 1,
            "follow_up_date": "2026-03-01",
            "target_id": target_id,
        },
        headers=headers,
    )
    assert pipeline_response.status_code == 200
    pipeline_entry_id = pipeline_response.json()["id"]

    person_response = client.post(
        "/people",
        json={
            "full_name": "Jane Recruiter",
            "title": "Recruiter",
            "email": "jane@example.com",
            "linkedin_url": "https://www.linkedin.com/in/janerecruiter",
            "relationship_notes": "Met at career fair",
            "target_id": target_id,
        },
        headers=headers,
    )
    assert person_response.status_code == 200

    activity_response = client.post(
        "/activity",
        json={
            "body": "Sent follow-up email after applying",
            "pipeline_entry_id": pipeline_entry_id,
        },
        headers=headers,
    )
    assert activity_response.status_code == 200

    overview_response = client.get("/insights/overview", headers=headers)
    assert overview_response.status_code == 200
    data = overview_response.json()
    assert data["total_targets"] == 1
    assert data["total_pipeline_entries"] == 1
    assert data["total_people"] == 1
    assert data["total_activity_logs"] == 1
    assert data["follow_up_due"] == 1
    assert data["stage_breakdown"]["applied"] == 1

    due_response = client.get("/pipeline?follow_up_due=true", headers=headers)
    assert due_response.status_code == 200
    due_data = due_response.json()
    assert len(due_data) == 1
    assert due_data[0]["position_title"] == "Software Engineering Intern"
