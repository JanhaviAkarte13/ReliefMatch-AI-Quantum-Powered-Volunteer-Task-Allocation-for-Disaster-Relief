from scipy.optimize import COBYLA
from qiskit.primitives import StatevectorSampler
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from optimizer import calculate_score


def quantum_allocate(volunteers, tasks):

    qp = QuadraticProgram()

    variables = []

    for v in volunteers:
        for t in tasks:
            name = f"x_{v['id']}_{t['id']}"
            qp.binary_var(name=name)
            variables.append((name, v, t))

    objective = {}

    for name, volunteer, task in variables:
        score = calculate_score(volunteer, task)
        objective[name] = -score

    qp.minimize(linear=objective)

    sampler = StatevectorSampler()

    # Classical optimizer for QAOA
    classical_optimizer = COBYLA(maxiter=100)

    qaoa = QAOA(
        sampler=sampler,
        optimizer=classical_optimizer,
        reps=2
    )

    quantum_optimizer = MinimumEigenOptimizer(qaoa)

    result = quantum_optimizer.solve(qp)

    allocation = []

    for variable in result.variables:
        if result.variable_values[variable.name] == 1:
            allocation.append(variable.name)

    return allocation