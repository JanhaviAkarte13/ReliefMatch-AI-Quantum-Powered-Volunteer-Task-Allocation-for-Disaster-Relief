def calculate_fit_score(volunteer, task):
    score = 0

    # -------------------------
    # 1. Availability
    # -------------------------
    if volunteer["availability"].lower() == "available":
        score += 30

    elif volunteer["availability"].lower() == "assigned":
        score += 10

    else:
        score += 0


    # -------------------------
    # 2. Skill matching
    # -------------------------
    volunteer_skills = {
        skill.strip().lower()
        for skill in str(volunteer["skills"]).split(";")
    }

    required_skills = {
        skill.strip().lower()
        for skill in str(task["required_skills"]).split(";")
        if skill.strip()
    }


    if required_skills:

        matched_skills = (
            volunteer_skills.intersection(required_skills)
        )

        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 40

        score += skill_score


    # -------------------------
    # 3. Location matching
    # -------------------------
    volunteer_location = str(
        volunteer["location"]
    ).strip().lower()

    task_location = str(
        task["location"]
    ).strip().lower()

    if volunteer_location == task_location:
        score += 20


    # -------------------------
    # 4. Urgency contribution
    # -------------------------
    urgency = float(task.get("urgency_score", 0))

    score += urgency * 0.10


    return round(score, 2)