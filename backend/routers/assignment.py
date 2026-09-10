"""
routers/assignment.py
The orchestration endpoint: POST /assignments/generate

Pipeline:
  1. Load unresolved tasks + available volunteers from the DB.
  2. AI urgency scoring        -> ai_urgency_score(task)            [Member 3]
  3. Build the fit-score matrix -> compute_fit_score(volunteer, task) [Member 3]
  4. Quantum optimization       -> quantum_optimize(...)             [Member 4]
  5. Classical baseline         -> classical_optimize(...)           [Member 4]
  6. Return a combined list of assignments + comparison metrics, shaped
     to match the frontend's apiClient.js.

Everything marked PLACEHOLDER is a stand-in until Member 3 (AI) and
Member 4 (Quantum) hand over their real functions - see the comments
below for exactly how to swap them in.
"""

import time
from typing import Dict, List, Tuple

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.task import Task
from models.volunteer import Volunteer
from schemas.schemas import AssignmentEntry, AssignmentResponse, ComparisonBlock, SolverSummary

from ai_module.fit_score import calculate_fit_score
from ai_module.urgency_model import predict_urgency

router = APIRouter(tags=["Assignment"])


# ==============================================================================
# PLACEHOLDER 1 - AI urgency scoring (Member 3 will replace this)
# ==============================================================================

def ai_urgency_score(task: Task) -> float:
    task_dict = {
        "severity": task.severity,
        "population_affected": task.people_affected,
        "hours_since_reported": task.reported_minutes_ago / 60,
    }
    return predict_urgency(task_dict)


# ==============================================================================
# PLACEHOLDER 2 - Volunteer-task fit score (Member 3 will replace this)
# ==============================================================================

def compute_fit_score(volunteer: Volunteer, task: Task, urgency_score: float) -> float:
    volunteer_skills = [s.strip() for s in volunteer.skills.split(",") if s.strip()]
    matching_skill = task.task_type if task.task_type in volunteer_skills else (
        volunteer_skills[0] if volunteer_skills else ""
    )

    volunteer_dict = {
        "id": volunteer.id,
        "skill": matching_skill,
        "latitude": volunteer.latitude or 0.0,
        "longitude": volunteer.longitude or 0.0,
        "available": volunteer.is_available,
    }
    task_dict = {
        "task_id": task.id,
        "required_skill": task.task_type,
        "latitude": task.latitude or 0.0,
        "longitude": task.longitude or 0.0,
        "urgency_score": urgency_score,
    }
    return calculate_fit_score(volunteer_dict, task_dict)


# ==============================================================================
# PLACEHOLDER 3 - Quantum optimizer (Member 4 will replace this)
# ==============================================================================
def quantum_optimize(
    fit_matrix: Dict[Tuple[int, int], float],
    task_ids: List[int],
    volunteer_ids: List[int],
) -> Tuple[List[Tuple[int, int, float]], dict]:
    sorted_pairs = sorted(fit_matrix.items(), key=lambda kv: kv[1], reverse=True)
    used_tasks, used_volunteers = set(), set()
    assignments: List[Tuple[int, int, float]] = []
    for (task_id, volunteer_id), score in sorted_pairs:
        if task_id in used_tasks or volunteer_id in used_volunteers:
            continue
        assignments.append((task_id, volunteer_id, score))
        used_tasks.add(task_id)
        used_volunteers.add(volunteer_id)
    return assignments, {"note": "PLACEHOLDER greedy solver standing in for QAOA"}


# ==============================================================================
# PLACEHOLDER 4 - Classical baseline optimizer (Member 4 will replace this)
# ==============================================================================
def classical_optimize(
    fit_matrix: Dict[Tuple[int, int], float],
    task_ids: List[int],
    volunteer_ids: List[int],
) -> Tuple[List[Tuple[int, int, float]], dict]:
    sorted_pairs = sorted(fit_matrix.items(), key=lambda kv: kv[1], reverse=True)
    used_tasks, used_volunteers = set(), set()
    assignments: List[Tuple[int, int, float]] = []
    for (task_id, volunteer_id), score in sorted_pairs:
        if task_id in used_tasks or volunteer_id in used_volunteers:
            continue
        assignments.append((task_id, volunteer_id, score))
        used_tasks.add(task_id)
        used_volunteers.add(volunteer_id)
    return assignments, {"note": "PLACEHOLDER greedy solver standing in for Hungarian algorithm"}


# ==============================================================================
# Orchestration endpoint - matches frontend's generateAssignment() call
# ==============================================================================
@router.post("/assignments/generate", response_model=AssignmentResponse)
def generate_assignment(db: Session = Depends(get_db)):
    tasks: List[Task] = db.query(Task).filter(Task.is_resolved == False).all()  # noqa: E712
    volunteers: List[Volunteer] = db.query(Volunteer).filter(Volunteer.is_available == True).all()  # noqa: E712

    if not tasks:
        raise HTTPException(status_code=400, detail="No unresolved tasks to assign.")
    if not volunteers:
        raise HTTPException(status_code=400, detail="No available volunteers to assign.")

    # lookups for building readable output later
    task_lookup = {t.id: t for t in tasks}
    volunteer_lookup = {v.id: v for v in volunteers}

    # --- AI urgency scoring ---
    urgency_scores: Dict[int, float] = {}
    for task in tasks:
        score = ai_urgency_score(task)
        task.urgency_score = score
        urgency_scores[task.id] = score
    db.commit()

    # --- fit-score matrix ---
    fit_matrix: Dict[Tuple[int, int], float] = {}
    for task in tasks:
        for volunteer in volunteers:
            fit_matrix[(task.id, volunteer.id)] = compute_fit_score(volunteer, task, urgency_scores[task.id])

    task_ids = [t.id for t in tasks]
    volunteer_ids = [v.id for v in volunteers]

    # --- quantum ---
    q_start = time.perf_counter()
    quantum_assignments, _ = quantum_optimize(fit_matrix, task_ids, volunteer_ids)
    quantum_ms = (time.perf_counter() - q_start) * 1000

    # --- classical ---
    c_start = time.perf_counter()
    classical_assignments, _ = classical_optimize(fit_matrix, task_ids, volunteer_ids)
    classical_ms = (time.perf_counter() - c_start) * 1000

    def build_entries(assignments, method: str) -> List[AssignmentEntry]:
        entries = []
        for task_id, volunteer_id, score in assignments:
            entries.append(AssignmentEntry(
                volunteer_id=volunteer_id,
                volunteer_name=volunteer_lookup[volunteer_id].name,
                task_id=task_id,
                task_location=task_lookup[task_id].location,
                fit_score=score,
                method=method,
            ))
        return entries

    quantum_entries = build_entries(quantum_assignments, "quantum")
    classical_entries = build_entries(classical_assignments, "classical")

    comparison = ComparisonBlock(
        quantum=SolverSummary(
            fit_score_total=round(sum(e.fit_score for e in quantum_entries), 2),
            tasks_covered=len(quantum_entries),
            solve_time_ms=round(quantum_ms, 3),
        ),
        classical=SolverSummary(
            fit_score_total=round(sum(e.fit_score for e in classical_entries), 2),
            tasks_covered=len(classical_entries),
            solve_time_ms=round(classical_ms, 3),
        ),
    )

    return AssignmentResponse(
        assignments=quantum_entries + classical_entries,
        comparison=comparison,
    )