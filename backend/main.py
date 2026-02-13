from fastapi import FastAPI, HTTPException
from typing import List
from backend.database import create_table
from backend.models import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse
)
import backend.crud as crud

app = FastAPI(
    title="Job Application Tracker API",
    description="REST API to manage job applications",
    version="1.0.0"
)

# Create DB table on startup
@app.on_event("startup")
def startup_event():
    create_table()


# ---------------- CREATE ----------------
@app.post("/applications", response_model=ApplicationResponse)
def create_application(application: ApplicationCreate):
    app_id = crud.create_application(application)
    return ApplicationResponse(id=app_id, **application.dict())


# ---------------- READ ALL ----------------
@app.get("/applications", response_model=List[ApplicationResponse])
def get_applications():
    rows = crud.get_all_applications()
    return [
        ApplicationResponse(
            id=row[0],
            company=row[1],
            role=row[2],
            location=row[3],
            date_applied=row[4],
            status=row[5],
            notes=row[6],
        )
        for row in rows
    ]


# ---------------- READ ONE ----------------
@app.get("/applications/{app_id}", response_model=ApplicationResponse)
def get_application(app_id: int):
    row = crud.get_application_by_id(app_id)
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")

    return ApplicationResponse(
        id=row[0],
        company=row[1],
        role=row[2],
        location=row[3],
        date_applied=row[4],
        status=row[5],
        notes=row[6],
    )


# ---------------- UPDATE ----------------
@app.put("/applications/{app_id}")
def update_application(app_id: int, update: ApplicationUpdate):
    row = crud.get_application_by_id(app_id)
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")

    crud.update_application_status(app_id, update.status)
    return {"message": "Application status updated"}


# ---------------- DELETE ----------------
@app.delete("/applications/{app_id}")
def delete_application(app_id: int):
    row = crud.get_application_by_id(app_id)
    if not row:
        raise HTTPException(status_code=404, detail="Application not found")

    crud.delete_application(app_id)
    return {"message": "Application deleted"}
