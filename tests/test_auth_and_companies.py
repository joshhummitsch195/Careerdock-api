from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

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



def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "pytest@example.com",
            "full_name": "Pytest User",
            "password": "123456",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "pytest@example.com"
    assert data["full_name"] == "Pytest User"



def test_login():
    response = client.post(
        "/auth/login",
        data={
            "username": "pytest@example.com",
            "password": "123456",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"



def test_create_target():
    login_response = client.post(
        "/auth/login",
        data={
            "username": "pytest@example.com",
            "password": "123456",
        },
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/targets",
        json={
            "name": "Pytest Company",
            "website": "https://example.com",
            "location": "Test City",
            "focus_area": "Created during pytest",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pytest Company"
    assert data["owner_id"] == 1
