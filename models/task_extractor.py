from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re
import pickle
import pandas as pd

MODEL_PATH = "models/task_extractor.pkl"
TASK_CSV = "models/task_training_data.csv"

# train in terminal 
# python -c "from models.task_extractor import TaskExtractor; TaskExtractor().train()"

class TaskExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1
        )
        self.model = LogisticRegression(max_iter=500)

    def train(self):
        data = pd.read_csv(TASK_CSV)
        data = data.sample(frac=1, random_state=42)  # shuffle
        sentences = data["sentence"].tolist()
        labels = data["is_task"].tolist()

        # Fit vectorizer + model
        X = self.vectorizer.fit_transform(sentences)
        self.model.fit(X, labels)

        # Save model + vectorizer
        with open(MODEL_PATH, "wb") as f:
            pickle.dump((self.vectorizer, self.model), f)

        print("Task extraction model trained and saved.")

    def extract(self, description):
        # Split description into sentences
        raw = re.split(r"[.\n•]", description)
        sentences = [s.strip() for s in raw if len(s.strip()) > 5]

        # Load model
        with open(MODEL_PATH, "rb") as f:
            vectorizer, model = pickle.load(f)

        X = vectorizer.transform(sentences)
        preds = model.predict(X)

        # Return only sentences classified as tasks
        return [s for s, p in zip(sentences, preds) if p == 1]
