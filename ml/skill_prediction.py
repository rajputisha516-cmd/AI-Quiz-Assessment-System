import pandas as pd

def predict_skill_level(csv_path="data/user_attempts.csv"):
    df = pd.read_csv(csv_path)

    total_attempts = len(df)

    # ---------- GATE 1: very few attempts ----------
    if total_attempts < 6:
        return {
            "show_level": False,
            "message": "Please attempt at least 6 questions to get a meaningful assessment."
        }

    # ---------- FEATURE COMPUTATION ----------
    accuracy = df["correct"].mean()

    difficulties = df["difficulty"].tolist()
    if "hard" in difficulties:
        max_difficulty = "hard"
    elif "medium" in difficulties:
        max_difficulty = "medium"
    else:
        max_difficulty = "easy"

    hard_df = df[df["difficulty"] == "hard"]
    hard_accuracy = hard_df["correct"].mean() if not hard_df.empty else 0

    # ---------- SKILL RULES (UNCHANGED CORE LOGIC) ----------
    if accuracy < 0.5 or max_difficulty == "easy":
        level = "Beginner"
    elif accuracy >= 0.75 and max_difficulty == "hard" and hard_accuracy >= 0.5:
        level = "Advanced"
    else:
        level = "Intermediate"

    # ---------- GATE 2: enough attempts but still improving ----------
    if total_attempts < 15:
        return {
            "show_level": True,
            "level": level,
            "note": "Attempt more questions for a stronger assessment."
        }

    # ---------- STRONG SIGNAL ----------
    return {
        "show_level": True,
        "level": level
    }
