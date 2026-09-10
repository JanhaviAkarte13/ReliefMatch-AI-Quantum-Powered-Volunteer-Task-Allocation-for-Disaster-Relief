"""
routers/tasks.py
CRUD endpoints for relief tasks. Field names match the frontend's expected
shape (type, population_affected) - see schemas.py for the DB<->API mapping.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.task import Task
from schemas.schemas import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("", response_model=TaskOut, status_code=201)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        task_type=payload.type,
        location=payload.location,
        severity=payload.severity,
        people_affected=payload.population_affected,
        latitude=payload.latitude,
        longitude=payload.longitude,
        reported_minutes_ago=payload.reported_minutes_ago,
        description=payload.description,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return TaskOut.from_orm_obj(task)


@router.get("", response_model=List[TaskOut])
def list_tasks(include_resolved: bool = False, db: Session = Depends(get_db)):
    query = db.query(Task)
    if not include_resolved:
        query = query.filter(Task.is_resolved == False)  # noqa: E712
    tasks = query.order_by(Task.id).all()
    return [TaskOut.from_orm_obj(t) for t in tasks]


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskOut.from_orm_obj(task)


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if payload.type is not None:
        task.task_type = payload.type
    if payload.location is not None:
        task.location = payload.location
    if payload.severity is not None:
        task.severity = payload.severity
    if payload.population_affected is not None:
        task.people_affected = payload.population_affected
    if payload.latitude is not None:
        task.latitude = payload.latitude
    if payload.longitude is not None:
        task.longitude = payload.longitude
    if payload.reported_minutes_ago is not None:
        task.reported_minutes_ago = payload.reported_minutes_ago
    if payload.description is not None:
        task.description = payload.description
    if payload.is_resolved is not None:
        task.is_resolved = payload.is_resolved

    db.commit()
    db.refresh(task)
    return TaskOut.from_orm_obj(task)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None