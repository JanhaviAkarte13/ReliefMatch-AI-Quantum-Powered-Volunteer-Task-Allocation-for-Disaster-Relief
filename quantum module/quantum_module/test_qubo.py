from qubo_model import create_assignment_qubo


fit_matrix = [
    [0.90, 0.40, 0.70],
    [0.60, 0.95, 0.30],
    [0.50, 0.60, 0.85]
]

qp = create_assignment_qubo(fit_matrix)

print(qp)