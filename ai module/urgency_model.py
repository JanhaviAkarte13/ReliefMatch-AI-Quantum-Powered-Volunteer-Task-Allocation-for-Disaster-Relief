import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")


def predict_urgency(task):
    model = joblib.load(MODEL_PATH)

    data = pd.DataFrame([{
        "severity": task["severity"],
        "population_affected": task["population_affected"]
    }])

    prediction = model.predict(data)[0]

    return round(float(prediction), 2)


if __name__ == "__main__":
    test_task = {
        "severity": 8,
        "population_affected": 300
    }

    result = predict_urgency(test_task)

    print("Predicted Urgency Score:", result)