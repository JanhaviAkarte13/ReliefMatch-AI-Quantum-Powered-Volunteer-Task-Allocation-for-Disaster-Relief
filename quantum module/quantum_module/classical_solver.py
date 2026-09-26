import time
import numpy as np
from scipy.optimize import linear_sum_assignment


def classical_assignment(fit_matrix):
    """
    Solve the volunteer-task assignment problem
    using the classical Hungarian algorithm.
    """

    # Convert input to NumPy array
    fit_matrix = np.asarray(fit_matrix, dtype=float)

    # Basic validation
    if fit_matrix.ndim != 2:
        raise ValueError("fit_matrix must be a 2D matrix")

    if fit_matrix.size == 0:
        raise ValueError("fit_matrix cannot be empty")

    # Hungarian algorithm minimizes cost.
    # Our matrix contains fit scores that we want to maximize.
    # Therefore, convert fit scores to negative costs.
    cost_matrix = -fit_matrix

    # Start timing
    start_time = time.perf_counter()

    # Solve assignment problem
    volunteer_indices, task_indices = linear_sum_assignment(
        cost_matrix
    )

    # Stop timing
    solve_time = time.perf_counter() - start_time

    # Store assignments
    assignments = []

    for volunteer, task in zip(
        volunteer_indices,
        task_indices
    ):
        assignments.append({
            "volunteer": int(volunteer),
            "task": int(task),
            "fit_score": float(fit_matrix[volunteer, task])
        })

    # Calculate total fit score
    total_fit_score = sum(
        assignment["fit_score"]
        for assignment in assignments
    )

    return {
        "assignments": assignments,
        "total_fit_score": float(total_fit_score),
        "tasks_covered": len(assignments),
        "solve_time": solve_time
    }