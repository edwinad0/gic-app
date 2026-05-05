import pickle
import joblib 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# to train in terminal: 
# python -c "from models.classifier import train_model; train_model()"

MODEL_PATH = "models/task_classifier.pkl"
TRAINING_CSV = "models/training_data.csv"

def train_model():
    df = pd.read_csv(TRAINING_CSV)
    df = df.sample(frac=1, random_state=42)  # shuffle

    texts = df["Task"].tolist()
    labels = df["Classification"].tolist()

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)  # bigrams improve accuracy
    )
    X = vectorizer.fit_transform(texts)

    clf = LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    )
    clf.fit(X, labels)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump((vectorizer, clf), f)

    print("Model trained and saved.")

def classify_task(text):
    vectorizer, clf = joblib.load(MODEL_PATH)
    X = vectorizer.transform([text])
    return clf.predict(X)[0]
