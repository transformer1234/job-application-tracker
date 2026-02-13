from pydantic import BaseModel
from typing import Optional
from datetime import date


# Shared fields
class ApplicationBase(BaseModel):
    company: str
    role: str
    location: Optional[str] = None
    date_applied: date
    status: str
    notes: Optional[str] = None


# Request body for creating an application
class ApplicationCreate(ApplicationBase):
    pass


# Request body for updating application status
class ApplicationUpdate(BaseModel):
    status: str


# Response model (what API returns)
class ApplicationResponse(ApplicationBase):
    id: int

    class Config:
        orm_mode = True
