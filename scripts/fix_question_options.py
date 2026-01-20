import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

QUESTION_FILES = [
    "python_questions.csv",
    "ml_questions.csv",
    "sql_questions.csv",
    "combined_questions.csv"
]

def clean_csv(file_path):
    df = pd.read_csv(file_path)

    option_cols = ["option_a", "option_b", "option_c", "option_d"]

    def fix_row(row):
        options = {
            "a": row["option_a"],
            "b": row["option_b"],
            "c": row["option_c"],
            "d": row["option_d"]
        }

        valid_options = {
            k: v for k, v in options.items()
            if isinstance(v, str) and v.strip()
        }

        # fix incorrect correct_option
        if row["correct_option"] not in valid_options:
            row["correct_option"] = list(valid_options.keys())[0]

        # normalize empty options
        for col in option_cols:
            if not isinstance(row[col], str) or not row[col].strip():
                row[col] = ""

        return row

    df = df.apply(fix_row, axis=1)
    df.to_csv(file_path, index=False)

    print(f"✅ Fixed option issues in: {file_path.name}")

if __name__ == "__main__":
    for fname in QUESTION_FILES:
        fpath = DATA_DIR / fname
        if fpath.exists():
            clean_csv(fpath)
        else:
            print(f"⚠️ File not found, skipped: {fname}")

    print("🎉 All question option issues fixed successfully")
