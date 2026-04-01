# CareerDock API

I built CareerDock API, a FastAPI backend for tracking internships, job applications, recruiter contacts, and follow-up activity.

## Overview

This project helps a user stay organized during a job search by saving companies, tracking application stages, storing contacts, logging outreach activity, and viewing a simple dashboard summary.

## What I Built

With this API, a user can:
- register and log in
- save target companies
- track applications through different stages
- store recruiter or referral contacts
- log follow-up notes and activity
- view a simple overview of their search progress

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- python-jose
- Passlib / bcrypt
- Pytest

## Features

- user registration and login
- JWT-based authentication
- CRUD endpoints for companies, applications, contacts, and notes
- filtering and pagination for selected routes
- dashboard summary endpoint with stage counts and follow-up information
- automated tests with Pytest

## Why I Built It

I wanted to build a backend project that felt more practical than a basic tutorial app and was directly related to internship and job searching. This project helped me practice API design, authentication, working with database models, and testing backend functionality.

## Main Endpoints

- `/auth/register`
- `/auth/login`
- `/auth/me`
- `/targets`
- `/pipeline`
- `/people`
- `/activity`
- `/insights/overview`

## Project Structure

```text
app/
  api/
    deps.py
    routes/
      auth.py
      companies.py
      applications.py
      contacts.py
      dashboard.py
      notes.py
  core/
    config.py
    database.py
    security.py
  models/
    user.py
    company.py
    application.py
    contact.py
    note.py
  schemas/
    user.py
    auth.py
    company.py
    application.py
    contact.py
    note.py
  main.py
tests/
requirements.txt
README.md
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Example Workflow

1. Register a user
2. Log in and copy the bearer token
3. Create a target company
4. Add an application entry for a role
5. Save a recruiter or referral contact
6. Add notes after outreach or interviews
7. Check the overview endpoint

## Testing

```bash
pytest -q
```

## Future Improvements

- move from SQLite to Postgres
- add Alembic migrations
- add Docker
- add a small frontend later
- deploy it publicly
