from fit_score import calculate_fit_score


def test_fit_score():

    volunteer = {
        "id": "VOL-0001",
        "name": "Test Volunteer",
        "location": "Nagpur",
        "skills": "Medical; Food Distribution",
        "availability": "Available"
    }

    task = {
        "id": "TASK-0001",
        "location": "Nagpur",
        "task_type": "Medical",
        "status": "Pending",
        "severity": 8,
        "required_skills": "Medical",
        "population_affected": 300,
        "urgency_score": 75
    }

    score = calculate_fit_score(
        volunteer,
        task
    )

    print("Fit score:", score)

    assert score > 0


if __name__ == "__main__":
    test_fit_score()
    print("AI module test passed.")