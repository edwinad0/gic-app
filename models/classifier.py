import pickle
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "models/task_classifier.pkl"
TRAINING_CSV = "models/training_data/training_data.csv"
EVAL_CSV = "models/test_data/test_classifier.csv"

# train in terminal 
# python -c "from models.classifier import TaskClassifier; TaskClassifier().train()"

# evaluation in terminal
# python -c "from models.classifier import TaskClassifier; TaskClassifier().evaluate_on_file()"

class TaskClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )
        self.model = LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )

    def train(self):
        df = pd.read_csv(TRAINING_CSV)
        df = df.sample(frac=1, random_state=42)

        texts = df["Task"].tolist()
        labels = df["Classification"].tolist()

        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

        with open(MODEL_PATH, "wb") as f:
            pickle.dump((self.vectorizer, self.model), f)

        print("Task classifier trained and saved.")

    def predict(self, text):
        # Load model fresh each time (safe for Dash multi‑worker)
        with open(MODEL_PATH, "rb") as f:
            vectorizer, model = pickle.load(f)

        X = vectorizer.transform([text])
        return model.predict(X)[0]
