import pandas as pd
import os

CSV_PATH = "models/training_data.csv"

def get_training_data():
    if not os.path.exists(CSV_PATH):
        return []

    df = pd.read_csv(CSV_PATH)

    # Add ID column if missing
    if "id" not in df.columns:
        df.insert(0, "id", range(1, len(df) + 1))
        df.to_csv(CSV_PATH, index=False)

    return df.to_dict("records")

def insert_training_sample(task, classification):
    df = pd.read_csv(CSV_PATH)

    new_id = df["id"].max() + 1 if len(df) else 1

    df.loc[len(df)] = [new_id, task, classification]
    df.to_csv(CSV_PATH, index=False)

    return new_id


def update_training_sample(sample_id, task, classification):
    df = pd.read_csv(CSV_PATH)

    df.loc[df["id"] == sample_id, "Task"] = task
    df.loc[df["id"] == sample_id, "Classification"] = classification

    df.to_csv(CSV_PATH, index=False)


def delete_training_sample(sample_id):
    df = pd.read_csv(CSV_PATH)

    df = df[df["id"] != sample_id]

    df.to_csv(CSV_PATH, index=False)
