import pickle
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

MODEL_PATH = "models/task_classifier.pkl"
TRAINING_CSV = "models/training_data/training_data.csv"
EVAL_CSV = "models/test_data/test_classifier.csv"

# train in terminal 
# python -c "from models.classifier import TaskClassifier; TaskClassifier().train()"

# evaluation in terminal
# python -c "from models.classifier import TaskClassifier; TaskClassifier().evaluate()"

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

    def predict(self, text, threshold=0.35):
        """
        Predict Task Classification
        """
        with open(MODEL_PATH, "rb") as f:
            vectorizer, model = pickle.load(f)

        X = vectorizer.transform([text])
        probs = model.predict_proba(X)[0]

        pred_class = model.classes_[probs.argmax()]

        return pred_class
    
    def predict_with_confidence(self, text):
        """
        Returns:
        {
            "label": predicted_class,
            "confidence": max_probability,
            "probs": {class: probability}
        }
        """
        with open(MODEL_PATH, "rb") as f:
            vectorizer, model = pickle.load(f)

        X = vectorizer.transform([text])
        probs = model.predict_proba(X)[0]

        classes = model.classes_
        max_idx = probs.argmax()
        label = classes[max_idx]
        confidence = float(probs[max_idx])

        prob_dict = {cls: float(p) for cls, p in zip(classes, probs)}

        return {
            "label": label,
            "confidence": confidence,
            "probs": prob_dict
        }
    
    def evaluate(self):
        # Load saved model
        with open(MODEL_PATH, "rb") as f:
            vectorizer, model = pickle.load(f)

        # Load evaluation dataset
        data = pd.read_csv(EVAL_CSV)
        data = data.sample(frac=1, random_state=42) # shuffle
        sentences = data["Task"].tolist()
        labels = data["Classification"].tolist()

        # Vectorise
        X = vectorizer.transform(sentences)

        # Predict
        preds = model.predict(X)

        # Metrics
        acc = accuracy_score(labels, preds)
        prec = precision_score(labels, preds, average="weighted")
        rec = recall_score(labels, preds, average="weighted")
        f1 = f1_score(labels, preds, average="weighted")

        print(f"Accuracy: {acc:.3f}")
        print(f"Precision: {prec:.3f}")
        print(f"Recall: {rec:.3f}")
        print(f"F1 Score: {f1:.3f}")
