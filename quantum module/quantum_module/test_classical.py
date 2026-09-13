from classical_solver import classical_assignment


fit_matrix = [
    [0.90, 0.40, 0.70],
    [0.60, 0.95, 0.30],
    [0.50, 0.60, 0.85]
]


result = classical_assignment(fit_matrix)


print("\nCLASSICAL HUNGARIAN RESULT")
print("==========================")

for assignment in result["assignments"]:
    print(
        f"Volunteer {assignment['volunteer']} "
        f"-> Task {assignment['task']} "
        f"(fit = {assignment['fit_score']:.2f})"
    )

print(f"\nTotal fit score: {result['total_fit_score']:.2f}")
print(f"Tasks covered: {result['tasks_covered']}")
print(f"Solve time: {result['solve_time']:.8f} seconds")