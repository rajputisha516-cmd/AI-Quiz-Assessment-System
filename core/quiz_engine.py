import pandas as pd

class QuizEngine:
    def __init__(self):
        self.files = {
            "Python": "data/python_questions.csv",
            "ML": "data/ml_questions.csv",
            "SQL": "data/sql_questions.csv",
            "Combined": "data/combined_questions.csv"
        }

        self.data = {}
        for skill, path in self.files.items():
            try:
                self.data[skill] = pd.read_csv(path)
            except FileNotFoundError:
                self.data[skill] = pd.DataFrame()

    def get_questions(self, subject, difficulty, asked_questions, n=1):
        df = self.data.get(subject)

        if df is None or df.empty:
            return []

        # Remove already asked questions
        if asked_questions:
            df = df[~df["question"].isin(asked_questions)]

        if df.empty:
            return []

        # Combined quiz → ignore difficulty
        if subject != "Combined":
            df = df[df["difficulty"] == difficulty]

        if df.empty:
            return []

        return df.sample(n=min(n, len(df))).to_dict("records")
