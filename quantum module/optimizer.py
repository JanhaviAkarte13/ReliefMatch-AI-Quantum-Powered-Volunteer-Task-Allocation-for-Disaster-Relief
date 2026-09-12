def calculate_score(volunteer, task):

    score = 0

    # Skill Matching
    if volunteer["skill"] == task["required_skill"]:
        score += 40

    # Same Location
    if volunteer["location"] == task["location"]:
        score += 20

    # Availability
    if volunteer["available"]:
        score += 10

    # AI Urgency
    score += task["urgency"] * 3

    return score