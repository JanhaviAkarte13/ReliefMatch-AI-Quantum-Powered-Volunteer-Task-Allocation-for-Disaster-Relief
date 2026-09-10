"""
schemas/schemas.py
Pydantic models for request/response bodies.
Field names here are chosen to match what the frontend's apiClient.js expects.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ---------- Task ----------

class TaskCreate(BaseModel):
    type: str = Field(..., examples=["medical"])
    location: str = Field(..., examples=["Sector 7, Riverside"])
    severity: int = Field(..., ge=1, le=10)
    population_affected: int = Field(0, ge=0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    reported_minutes_ago: int = Field(0, ge=0)
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    type: Optional[str] = None
    location: Optional[str] = None
    severity: Optional[int] = Field(None, ge=1, le=10)
    population_affected: Optional[int] = Field(None, ge=0)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    reported_minutes_ago: Optional[int] = None
    description: Optional[str] = None
    is_resolved: Optional[bool] = None


class TaskOut(BaseModel):
    id: int
    type: str
    location: str
    severity: int
    population_affected: int
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    reported_minutes_ago: int
    description: Optional[str] = None
    urgency_score: Optional[float] = None
    is_resolved: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm_obj(t):
        """Converts a DB Task (task_type/people_affected) to the API shape (type/population_affected)."""
        return TaskOut(
            id=t.id,
            type=t.task_type,
            location=t.location,
            severity=t.severity,
            population_affected=t.people_affected,
            latitude=t.latitude,
            longitude=t.longitude,
            reported_minutes_ago=t.reported_minutes_ago,
            description=t.description,
            urgency_score=t.urgency_score,
            is_resolved=t.is_resolved,
            created_at=t.created_at,
        )


# ---------- Volunteer ----------

class VolunteerCreate(BaseModel):
    name: str
    skills: List[str] = Field(default_factory=list)
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    availability: bool = True


class VolunteerUpdate(BaseModel):
    name: Optional[str] = None
    skills: Optional[List[str]] = None
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    availability: Optional[bool] = None


class VolunteerOut(BaseModel):
    id: int
    name: str
    skills: List[str]
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    availability: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_orm_obj(v):
        return VolunteerOut(
            id=v.id,
            name=v.name,
            skills=[s.strip() for s in v.skills.split(",") if s.strip()],
            location=v.location,
            latitude=v.latitude,
            longitude=v.longitude,
            availability=v.is_available,
            created_at=v.created_at,
        )


# ---------- Assignment (shape matches frontend's apiClient.js exactly) ----------

class AssignmentEntry(BaseModel):
    volunteer_id: int
    volunteer_name: str
    task_id: int
    task_location: str
    fit_score: float
    method: str  # "quantum" or "classical"


class SolverSummary(BaseModel):
    fit_score_total: float
    tasks_covered: int
    solve_time_ms: float


class ComparisonBlock(BaseModel):
    quantum: SolverSummary
    classical: SolverSummary


class AssignmentResponse(BaseModel):
    assignments: List[AssignmentEntry]
    comparison: ComparisonBlock