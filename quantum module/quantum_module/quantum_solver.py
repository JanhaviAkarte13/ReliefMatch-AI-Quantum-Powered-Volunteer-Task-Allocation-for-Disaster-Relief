import time
import numpy as np

from qiskit.primitives import StatevectorSampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.minimum_eigensolvers import QAOA
from qiskit_optimization.optimizers import COBYLA

from qubo_model import create_assignment_qubo


def quantum_assignment(fit_matrix):
    """
    Solve the volunteer-task assignment problem using QAOA.

    Parameters
    ----------
    fit_matrix : list or numpy.ndarray
        Rows    = volunteers
        Columns = tasks
        Values  = fit scores

    Returns
    -------
    dict
        Quantum assignment results.
    """

    # Convert input to NumPy array
    fit_matrix = np.asarray(fit_matrix, dtype=float)

    # Validate input
    if fit_matrix.ndim != 2:
        raise ValueError("fit_matrix must be a 2D matrix")

    if fit_matrix.size == 0:
        raise ValueError("fit_matrix cannot be empty")

    # --------------------------------------------------
    # Step 1: Create the assignment optimization problem
    # --------------------------------------------------

    qp = create_assignment_qubo(fit_matrix)

    # --------------------------------------------------
    # Step 2: Create quantum sampler
    #
    # StatevectorSampler is Qiskit's simulator-based
    # SamplerV2 implementation.
    # --------------------------------------------------

    sampler = StatevectorSampler(
        seed=123
    )

    # --------------------------------------------------
    # Step 3: Classical optimizer used to optimize
    # QAOA parameters
    # --------------------------------------------------

    classical_optimizer = COBYLA(
        maxiter=100
    )

    # --------------------------------------------------
    # Step 4: Create QAOA
    #
    # reps=1 means one QAOA layer.
    # This is intentionally small for our project.
    # --------------------------------------------------

    qaoa = QAOA(
        sampler=sampler,
        optimizer=classical_optimizer,
        reps=1
    )

    # --------------------------------------------------
    # Step 5: Connect QAOA to the optimization problem
    # --------------------------------------------------

    quantum_optimizer = MinimumEigenOptimizer(
        qaoa
    )

    # --------------------------------------------------
    # Step 6: Solve
    # --------------------------------------------------

    start_time = time.perf_counter()

    result = quantum_optimizer.solve(qp)

    solve_time = time.perf_counter() - start_time

    # --------------------------------------------------
    # Step 7: Extract assignments
    # --------------------------------------------------

    assignments = []

    num_volunteers, num_tasks = fit_matrix.shape

    for i in range(num_volunteers):

      for j in range(num_tasks):

        # Variables were created in row-major order:
        # x_0_0, x_0_1, x_0_2,
        # x_1_0, x_1_1, x_1_2, ...
        variable_index = i * num_tasks + j

        value = result.x[variable_index]

        if value > 0.5:

            assignments.append({
                "volunteer": int(i),
                "task": int(j),
                "fit_score": float(
                    fit_matrix[i, j]
                )
            })
    # --------------------------------------------------
    # Step 8: Calculate metrics
    # --------------------------------------------------

    total_fit_score = sum(
        assignment["fit_score"]
        for assignment in assignments
    )

    return {
     "assignments": assignments,
     "total_fit_score": float(total_fit_score),
     "tasks_covered": len(assignments),
     "solve_time": solve_time,
     "objective_value": float(result.fval)
}