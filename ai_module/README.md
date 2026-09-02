# ReliefMatch – AI Module

## Overview

The AI Module is a component of the **ReliefMatch** disaster relief system. It is responsible for:

- Predicting the urgency of disaster tasks using a Machine Learning model.
- Calculating the compatibility (fit score) between volunteers and disaster tasks.

This module is designed to integrate with the FastAPI backend and provide inputs for the Quantum Optimization Module.

---

# Project Structure

```
ai_module/
│
├── __init__.py
├── urgency_model.py
├── fit_score.py
├── generate_dataset.py
├── train.py
├── test_ai_module.py
├── requirements.txt
├── README.md
│
├── data/
│   └── synthetic_tasks.csv
│
└── models/
    └── model.pkl
```

---

# Technologies Used

- Python 3.12
- Scikit-learn
- Pandas
- NumPy
- Joblib

---

# Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

# AI Module Components

## 1. Urgency Prediction

Predicts the urgency score of a disaster task using a trained Random Forest Regression model.

### Function

```python
predict_urgency(task)
```

### Input

```python
task = {
    "severity": 8,
    "population_affected": 5000,
    "hours_since_reported": 6
}
```

### Output

```python
90.44
```

The urgency score ranges approximately between **0 and 100**, where a higher score indicates a more urgent disaster task.

---

## 2. Volunteer-Task Fit Score

Calculates how suitable a volunteer is for a specific disaster task.

### Function

```python
calculate_fit_score(volunteer, task)
```

### Volunteer Format

```python
volunteer = {
    "id": 1,
    "skill": "Medical",
    "latitude": 21.1458,
    "longitude": 79.0882,
    "available": True
}
```

### Task Format

```python
task = {
    "task_id": 101,
    "required_skill": "Medical",
    "latitude": 21.1600,
    "longitude": 79.0900,
    "urgency_score": 90.44
}
```

### Output

```python
97.13
```

The returned value represents the volunteer-task compatibility score.

---

# Fit Score Formula

The fit score is calculated as:

```
Fit Score =
0.50 × Skill Score
+ 0.30 × Distance Score
+ 0.20 × Urgency Score
```

Where:

- **Skill Score** → Based on required skill matching.
- **Distance Score** → Computed using the Haversine Distance Formula.
- **Urgency Score** → Predicted by the AI model.

---

# Machine Learning Model

### Algorithm

- Random Forest Regressor

### Input Features

- Severity Score
- Population Affected
- Hours Since Reported

### Output

- Predicted Urgency Score

---

# Integration Workflow

```
User
   │
   ▼
Frontend
   │
   ▼
FastAPI Backend
   │
   ├── predict_urgency(task)
   │
   ▼
Urgency Score
   │
   ▼
calculate_fit_score(volunteer, task)
   │
   ▼
Volunteer Fit Score
   │
   ▼
Quantum Optimization Module
```

---

# Example Usage

```python
from urgency_model import predict_urgency
from fit_score import calculate_fit_score

# Disaster task
task = {
    "severity": 8,
    "population_affected": 5000,
    "hours_since_reported": 6
}

# Predict urgency
urgency = predict_urgency(task)

# Add urgency score for fit score calculation
task_for_fit = {
    "task_id": 101,
    "required_skill": "Medical",
    "latitude": 21.1600,
    "longitude": 79.0900,
    "urgency_score": urgency
}

# Volunteer information
volunteer = {
    "id": 1,
    "skill": "Medical",
    "latitude": 21.1458,
    "longitude": 79.0882,
    "available": True
}

# Calculate compatibility
fit_score = calculate_fit_score(volunteer, task_for_fit)

print("Urgency Score:", urgency)
print("Fit Score:", fit_score)
```

---

# Notes

- This module is intended for the ReliefMatch prototype.
- Distance calculations are performed using latitude and longitude coordinates.
- In the prototype, location names entered by users can be converted to coordinates by the backend before invoking this module.
- The AI module focuses only on prediction and scoring; it does not perform volunteer assignment.

---

# Authors

**Project:** ReliefMatch – AI & Quantum Powered Volunteer Allocation for Disaster Relief

**Module:** AI Module (Member 3)

**Developer:** Khushboo Chourasia

**Department:** Computer Science & Engineering (Artificial Intelligence)

**College:** G. H. Raisoni College of Engineering, Nagpur