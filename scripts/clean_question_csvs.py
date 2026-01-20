import pandas as pd
import os

DATA_FOLDER = "data"

for file in os.listdir(DATA_FOLDER):
    if file.endswith("_questions.csv"):
        file_path = os.path.join(DATA_FOLDER, file)

        df = pd.read_csv(file_path)

        before = len(df)
        df = df.drop_duplicates()
        after = len(df)

        df.to_csv(file_path, index=False)

        print(f"{file}: {before - after} duplicate rows removed")

print("✅ All question CSV files cleaned successfully")
