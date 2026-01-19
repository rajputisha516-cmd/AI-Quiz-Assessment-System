import pandas as pd

def generate_features(csv_path="data/user_attempts.csv"):
    df = pd.read_csv(csv_path)

    if df.empty:
        return None

    total_questions = len(df)
    accuracy = df["correct"].mean()
    avg_time = df["time_taken"].mean()

    hard_df = df[df["difficulty"] == "hard"]
    hard_accuracy = hard_df["correct"].mean() if not hard_df.empty else 0

    speed_score = accuracy / avg_time if avg_time > 0 else 0

    features = {
        "total_questions": total_questions,
        "accuracy": round(accuracy, 2),
        "avg_time": round(avg_time, 2),
        "hard_accuracy": round(hard_accuracy, 2),
        "speed_score": round(speed_score, 2)
    }

    return features
