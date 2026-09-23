import os
import pandas as pd

from fit_score import calculate_fit_score
from urgency_model import predict_urgency


# -------------------------
# File paths
# -------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TASK_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "Dataset", "tasks.csv")
)

VOLUNTEER_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "Dataset", "volunteers.csv")
)


# -------------------------
# Load real datasets
# -------------------------

def load_data():

    tasks = pd.read_csv(TASK_PATH)
    volunteers = pd.read_csv(VOLUNTEER_PATH)

    return tasks, volunteers


# -------------------------
# Build small fit matrix
# -------------------------

def build_fit_matrix(tasks, volunteers):

    matrix = []

    for _, task in tasks.iterrows():

        task_dict = task.to_dict()

        # Predict urgency using trained ML model
        urgency = predict_urgency(task_dict)

        task_dict["urgency_score"] = urgency

        row = []

        for _, volunteer in volunteers.iterrows():

            volunteer_dict = volunteer.to_dict()

            score = calculate_fit_score(
                volunteer_dict,
                task_dict
            )

            row.append(score)

        matrix.append(row)

    return matrix


# -------------------------
# Main
# -------------------------

if __name__ == "__main__":

    # Load complete datasets
    tasks, volunteers = load_data()

    print("Total tasks available:", len(tasks))
    print("Total volunteers available:", len(volunteers))

    # Take only 5 tasks and 5 volunteers
    tasks_subset = tasks.head(5).copy()
    volunteers_subset = volunteers.head(5).copy()

    print("\nUsing subset:")
    print("Tasks:", len(tasks_subset))
    print("Volunteers:", len(volunteers_subset))

    # Build fit matrix
    matrix = build_fit_matrix(
        tasks_subset,
        volunteers_subset
    )

    print("\nFit Matrix")
    print("----------")

    fit_matrix = pd.DataFrame(
        matrix,
        index=tasks_subset["id"],
        columns=volunteers_subset["id"]
    )

    print(fit_matrix)

    print("\nFit matrix created successfully.")
    print(
        "Matrix size:",
        len(matrix),
        "x",
        len(matrix[0])
    )