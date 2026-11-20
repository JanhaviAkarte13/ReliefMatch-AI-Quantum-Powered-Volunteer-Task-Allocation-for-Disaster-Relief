import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Works whether model.pkl sits beside this file (GitHub "ai module" folder)
# or inside a "models" subfolder (backend/ai_module).
_candidates = [
    os.path.join(BASE_DIR, "model.pkl"),
    os.path.join(BASE_DIR, "models", "model.pkl"),
]
MODEL_PATH = next((p for p in _candidates if os.path.exists(p)), _candidates[0])
model = joblib.load(MODEL_PATH)


def predict_urgency(task: dict) -> float:
    severity = task["severity"]
    population = task["population_affected"]
    hours = task["hours_since_reported"]

    input_data = pd.DataFrame({
        "severity_score": [severity],
        "population_affected": [population],
        "hours_since_reported": [hours]
    })

    urgency = model.predict(input_data)[0]
    return round(float(urgency), 2)
