"""
models/volunteer.py
SQLAlchemy model for a volunteer.

skills is stored as a comma-separated string (e.g. "medical,driving") to keep
SQLite happy without needing a JSON column type. schemas.py exposes it to the
API as a proper List[str].
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func

from database import Base


class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    skills = Column(String, nullable=False, default="")   # comma-separated, e.g. "medical,rescue"

    location = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    is_available = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())