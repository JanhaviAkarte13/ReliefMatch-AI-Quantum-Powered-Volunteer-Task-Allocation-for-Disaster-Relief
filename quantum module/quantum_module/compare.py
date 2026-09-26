from quantum_solver import quantum_assignment
from classical_solver import classical_assignment


def compare_methods(fit_matrix):
    """
    Run both quantum QAOA and classical Hungarian
    algorithms on the same fit-score matrix.
    """

    # Run quantum method
    quantum_result = quantum_assignment(fit_matrix)

    # Run classical method
    classical_result = classical_assignment(fit_matrix)

    # Comparison metrics
    comparison = {
        "quantum_fit_score": quantum_result["total_fit_score"],
        "classical_fit_score": classical_result["total_fit_score"],

        "quantum_tasks_covered": quantum_result["tasks_covered"],
        "classical_tasks_covered": classical_result["tasks_covered"],

        "quantum_solve_time": quantum_result["solve_time"],
        "classical_solve_time": classical_result["solve_time"]
    }

    return {
        "quantum": quantum_result,
        "classical": classical_result,
        "comparison": comparison
    }