from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import re
import pickle
import pandas as pd

MODEL_PATH = "models/task_extractor.pkl"
TASK_CSV = "models/training_data/task_training_data.csv"
EVAL_CSV = "models/test_data/task_eval_data.csv"

# train in terminal 
# python -c "from models.task_extractor import TaskExtractor; TaskExtractor().train()"

# evaluation in terminal
# python -c "from models.task_extractor import TaskExtractor; TaskExtractor().evaluate()"

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

    def evaluate(self):
        # Load saved model
        with open(MODEL_PATH, "rb") as f:
            vectorizer, model = pickle.load(f)

        # Load evaluation dataset
        data = pd.read_csv(EVAL_CSV)
        sentences = data["sentence"].tolist()
        labels = data["is_task"].tolist()

        # Vectorise
        X = vectorizer.transform(sentences)

        # Predict
        preds = model.predict(X)

        # Metrics
        acc = accuracy_score(labels, preds)
        prec = precision_score(labels, preds)
        rec = recall_score(labels, preds)
        f1 = f1_score(labels, preds)

        print(f"Accuracy: {acc:.3f}")
        print(f"Precision: {prec:.3f}")
        print(f"Recall: {rec:.3f}")
        print(f"F1 Score: {f1:.3f}")

