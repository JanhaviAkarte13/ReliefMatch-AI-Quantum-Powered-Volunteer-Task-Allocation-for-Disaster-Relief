import os
import joblib
import pandas as pd

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build the absolute path to model.pkl
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")

# Load the trained model
model = joblib.load(MODEL_PATH)
import joblib
import pandas as pd

# Load the trained model
model = joblib.load("models/model.pkl")


def predict_urgency(task: dict) -> float:
    """
    Predict urgency score from a task dictionary.

    Expected task format:
    {
        "severity": 8,
        "population_affected": 5000,
        "hours_since_reported": 6
    }
    """

    # Extract values from dictionary
    severity = task["severity"]
    population = task["population_affected"]
    hours = task["hours_since_reported"]

    # Create DataFrame
    input_data = pd.DataFrame({
        "severity_score": [severity],
        "population_affected": [population],
        "hours_since_reported": [hours]
    })

    # Predict urgency
    urgency = model.predict(input_data)[0]

    return round(float(urgency), 2)


# Testing
if __name__ == "__main__":

    sample_task = {
        "severity": 8,
        "population_affected": 5000,
        "hours_since_reported": 6
    }

    score = predict_urgency(sample_task)

    print(f"Predicted Urgency Score: {score}")