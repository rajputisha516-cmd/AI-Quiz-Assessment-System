import pandas as pd

WINDOW_SIZE = 5
UPGRADE_ACCURACY = 0.8   # 80%
DOWNGRADE_ACCURACY = 0.4 # 40%
TIME_THRESHOLD = 10      # seconds


def get_next_difficulty(
    current_difficulty: str,
    subject: str,
    csv_path: str = "data/user_attempts.csv"
) -> str:
    """
    Decide next difficulty based on recent performance trend.
    """

    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return current_difficulty

    # filter same subject attempts
    df = df[df["subject"] == subject].tail(WINDOW_SIZE)

    # not enough data → no change
    if len(df) < WINDOW_SIZE:
        return current_difficulty

    accuracy = df["correct"].mean()
    avg_time = df["time_taken"].mean()

    # upgrade condition
    if accuracy >= UPGRADE_ACCURACY and avg_time <= TIME_THRESHOLD:
        return _upgrade(current_difficulty)

    # downgrade condition
    if accuracy <= DOWNGRADE_ACCURACY:
        return _downgrade(current_difficulty)

    # otherwise stable
    return current_difficulty


def _upgrade(level: str) -> str:
    if level == "easy":
        return "medium"
    if level == "medium":
        return "hard"
    return "hard"


def _downgrade(level: str) -> str:
    if level == "hard":
        return "medium"
    if level == "medium":
        return "easy"
    return "easy"
