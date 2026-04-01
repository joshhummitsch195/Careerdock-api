from fastapi import FastAPI

from app.api.routes import applications, auth, companies, contacts, dashboard, notes
from app.core.config import settings
from app.core.database import Base, engine
import app.models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)


@app.get("/")
def root():
    return {"message": "CareerDock API is running"}


app.include_router(auth.router)
app.include_router(companies.router)
app.include_router(applications.router)
app.include_router(notes.router)
app.include_router(contacts.router)
app.include_router(dashboard.router)
