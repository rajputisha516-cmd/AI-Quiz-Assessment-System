import csv
import os

def log_attempt(subject, topic, difficulty, correct, time_taken):
    """
    Logs a single quiz attempt to user_attempts.csv

    Parameters:
    - subject (str)
    - topic (str)
    - difficulty (str)
    - correct (bool)
    - time_taken (float)
    """

    file_path = "data/user_attempts.csv"

    # Check if file exists to write header only once
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                ["subject", "topic", "difficulty", "correct", "time_taken"]
            )

        writer.writerow([
            subject,
            topic,
            difficulty,
            correct,
            time_taken
        ])
