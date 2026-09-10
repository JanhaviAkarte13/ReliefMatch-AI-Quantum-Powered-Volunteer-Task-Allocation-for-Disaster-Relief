"""
models/task.py
SQLAlchemy model for a relief task.

urgency_score is nullable and starts as None - it only gets populated once
/generate-assignment runs the AI scoring function on this task.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func

from database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    task_type = Column(String, nullable=False)          # e.g. "medical", "food", "rescue", "shelter"
    location = Column(String, nullable=False)            # free-text location or "lat,lng"
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    severity = Column(Integer, nullable=False)            # raw severity input, e.g. 1-5 or 1-10
    people_affected = Column(Integer, nullable=False, default=0)
    reported_minutes_ago = Column(Integer, nullable=False, default=0)  # how long ago it was reported

    description = Column(String, nullable=True)

    # Filled in by the AI scoring function during /generate-assignment.
    urgency_score = Column(Float, nullable=True)

    is_resolved = Column(Boolean, default=False)          # marked True once a volunteer is assigned & done
    created_at = Column(DateTime(timezone=True), server_default=func.now())