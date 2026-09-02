from urgency_model import predict_urgency
from fit_score import calculate_fit_score

print("----- AI MODULE TEST -----")

# Step 1: Predict urgency
task = {
    "severity": 8,
    "population_affected": 5000,
    "hours_since_reported": 6
}

urgency = predict_urgency(task)

print("Urgency Score :", urgency)

# Step 2: Calculate fit score
volunteer = {
    "id": 1,
    "skill": "Medical",
    "latitude": 21.1458,
    "longitude": 79.0882,
    "available": True
}

task_for_fit = {
    "task_id": 101,
    "required_skill": "Medical",
    "latitude": 21.1600,
    "longitude": 79.0900,
    "urgency_score": urgency
}

fit = calculate_fit_score(volunteer, task_for_fit)

print("Fit Score :", fit)