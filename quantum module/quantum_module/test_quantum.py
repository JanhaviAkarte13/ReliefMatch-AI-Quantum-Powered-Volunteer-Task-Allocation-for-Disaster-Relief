from quantum_solver import quantum_assignment


fit_matrix = [
    [0.90, 0.40, 0.70],
    [0.60, 0.95, 0.30],
    [0.50, 0.60, 0.85]
]


print("Starting QAOA...")
print()


result = quantum_assignment(
    fit_matrix
)


print("QUANTUM QAOA RESULT")
print("===================")


for assignment in result["assignments"]:

    print(
        f"Volunteer {assignment['volunteer']} "
        f"-> Task {assignment['task']} "
        f"(fit = {assignment['fit_score']:.2f})"
    )


print()
print(
    f"Total fit score: "
    f"{result['total_fit_score']:.2f}"
)

print(
    f"Tasks covered: "
    f"{result['tasks_covered']}"
)

print(
    f"Solve time: "
    f"{result['solve_time']:.4f} seconds"
)