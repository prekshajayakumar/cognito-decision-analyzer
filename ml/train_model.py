import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "decision_model.pkl")


def generate_synthetic_dataset(n_samples=1200, random_state=42):
    np.random.seed(random_state)
    rows = []

    for _ in range(n_samples):
        label = np.random.choice(["Impulsive", "Balanced", "Analytical"])

        if label == "Impulsive":
            times = np.random.normal(loc=2.0, scale=0.6, size=8)
        elif label == "Balanced":
            times = np.random.normal(loc=4.0, scale=0.9, size=8)
        else:
            times = np.random.normal(loc=6.5, scale=1.2, size=8)

        times = np.clip(times, 0.7, 12)

        avg_time = np.mean(times)
        median_time = np.median(times)
        max_time = np.max(times)
        min_time = np.min(times)
        std_time = np.std(times)
        total_time = np.sum(times)

        hesitation_count = int(np.sum(times > 5))
        hesitation_ratio = hesitation_count / len(times)
        fast_count = int(np.sum(times < 3))
        slow_count = int(np.sum(times > 6))

        rows.append({
            "avg_response_time": avg_time,
            "median_response_time": median_time,
            "max_response_time": max_time,
            "min_response_time": min_time,
            "std_response_time": std_time,
            "total_time": total_time,
            "hesitation_count": hesitation_count,
            "hesitation_ratio": hesitation_ratio,
            "fast_answer_count": fast_count,
            "slow_answer_count": slow_count,
            "label": label,
        })

    return pd.DataFrame(rows)


def train_model():
    df = generate_synthetic_dataset()

    X = df.drop("label", axis=1)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)

    print("Model Accuracy:", round(accuracy * 100, 2), "%")
    print(classification_report(y_test, preds))

    joblib.dump(model, MODEL_PATH)
    print("Model saved to:", MODEL_PATH)


if __name__ == "__main__":
    train_model()
