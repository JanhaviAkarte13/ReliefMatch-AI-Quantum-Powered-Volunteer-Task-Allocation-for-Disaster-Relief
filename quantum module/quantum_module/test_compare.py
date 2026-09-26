from compare import compare_methods


fit_matrix = [
    [0.90, 0.40, 0.70],
    [0.60, 0.95, 0.30],
    [0.50, 0.60, 0.85]
]


result = compare_methods(fit_matrix)


print("\n================================")
print("RELIEFMATCH OPTIMIZATION RESULT")
print("================================")


print("\n--- QUANTUM QAOA ---")

for assignment in result["quantum"]["assignments"]:
    print(
        f"Volunteer {assignment['volunteer']} "
        f"-> Task {assignment['task']} "
        f"(fit = {assignment['fit_score']:.2f})"
    )

print(
    f"Total fit score: "
    f"{result['quantum']['total_fit_score']:.2f}"
)

print(
    f"Tasks covered: "
    f"{result['quantum']['tasks_covered']}"
)

print(
    f"Solve time: "
    f"{result['quantum']['solve_time']:.6f} seconds"
)


print("\n--- CLASSICAL HUNGARIAN ---")

for assignment in result["classical"]["assignments"]:
    print(
        f"Volunteer {assignment['volunteer']} "
        f"-> Task {assignment['task']} "
        f"(fit = {assignment['fit_score']:.2f})"
    )

print(
    f"Total fit score: "
    f"{result['classical']['total_fit_score']:.2f}"
)

print(
    f"Tasks covered: "
    f"{result['classical']['tasks_covered']}"
)

print(
    f"Solve time: "
    f"{result['classical']['solve_time']:.6f} seconds"
)


print("\n--- COMPARISON ---")

comparison = result["comparison"]

print(
    f"Quantum fit score: "
    f"{comparison['quantum_fit_score']:.2f}"
)

print(
    f"Classical fit score: "
    f"{comparison['classical_fit_score']:.2f}"
)

print(
    f"Quantum tasks covered: "
    f"{comparison['quantum_tasks_covered']}"
)

print(
    f"Classical tasks covered: "
    f"{comparison['classical_tasks_covered']}"
)

print(
    f"Quantum solve time: "
    f"{comparison['quantum_solve_time']:.6f} seconds"
)

print(
    f"Classical solve time: "
    f"{comparison['classical_solve_time']:.6f} seconds"
)