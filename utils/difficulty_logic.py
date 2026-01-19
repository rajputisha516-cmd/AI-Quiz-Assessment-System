def get_next_difficulty(current_difficulty, correct, time_taken):
    TIME_LIMITS = {
        "easy": 10,
        "medium": 18,
        "hard": 30
    }

    # EASY LEVEL
    if current_difficulty == "easy":
        if correct:
            return "medium"
        else:
            return "easy"

    # MEDIUM LEVEL
    if current_difficulty == "medium":
        if correct and time_taken <= TIME_LIMITS["medium"]:
            return "hard"
        elif correct:
            return "medium"
        else:
            return "easy"

    # HARD LEVEL
    if current_difficulty == "hard":
        if correct:
            return "hard"
        else:
            return "medium"

    return "easy"
