import math

# ---------------------------------
# Haversine Distance Function
# ---------------------------------

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance (in km) between two GPS coordinates.
    """

    R = 6371  # Earth's radius (km)

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


# ---------------------------------
# Volunteer-Task Fit Score
# ---------------------------------

def calculate_fit_score(volunteer: dict, task: dict) -> float:
    """
    Calculate the fit score between a volunteer and a disaster task.

    Volunteer Format
    ----------------
    {
        "id": 1,
        "skill": "Medical",
        "latitude": 21.1458,
        "longitude": 79.0882,
        "available": True
    }

    Task Format
    -----------
    {
        "task_id": 101,
        "required_skill": "Medical",
        "latitude": 21.1600,
        "longitude": 79.0900,
        "urgency_score": 90.44
    }

    Returns
    -------
    float
        Fit score between 0 and 100.
    """

    # -------------------------
    # Availability Check
    # -------------------------
    if not volunteer.get("available", False):
        return 0.0

    # -------------------------
    # Skill Match
    # -------------------------
    if volunteer["skill"].lower() == task["required_skill"].lower():
        skill_score = 100
    else:
        skill_score = 40

    # -------------------------
    # Distance Score
    # -------------------------
    distance = haversine_distance(
        volunteer["latitude"],
        volunteer["longitude"],
        task["latitude"],
        task["longitude"]
    )

    # Convert distance to score (0–100)
    distance_score = max(0, 100 - distance * 2)

    # -------------------------
    # Urgency Score
    # -------------------------
    urgency_score = task["urgency_score"]

    # -------------------------
    # Final Weighted Score
    # -------------------------
    fit_score = (
        0.50 * skill_score +
        0.30 * distance_score +
        0.20 * urgency_score
    )

    return round(fit_score, 2)


# ---------------------------------
# Testing
# ---------------------------------

if __name__ == "__main__":

    volunteer = {
        "id": 1,
        "skill": "Medical",
        "latitude": 21.1458,
        "longitude": 79.0882,
        "available": True
    }

    task = {
        "task_id": 101,
        "required_skill": "Medical",
        "latitude": 21.1600,
        "longitude": 79.0900,
        "urgency_score": 90.44
    }

    score = calculate_fit_score(volunteer, task)

    print("Volunteer Fit Score:", score)