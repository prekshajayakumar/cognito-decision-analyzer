import os
import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "decision_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "synthetic_decision_data.csv")


def generate_user_times(label, n_questions=8):
    if label == "Impulsive":
        base = np.random.normal(loc=3.1, scale=1.25, size=n_questions)
    elif label == "Balanced":
        base = np.random.normal(loc=4.4, scale=1.45, size=n_questions)
    else:
        base = np.random.normal(loc=5.7, scale=1.7, size=n_questions)

    # Realistic human inconsistency
    distraction_chance = np.random.rand(n_questions) < 0.15
    base[distraction_chance] += np.random.uniform(1.5, 4.0, size=distraction_chance.sum())

    guess_chance = np.random.rand(n_questions) < 0.10
    base[guess_chance] -= np.random.uniform(0.6, 1.5, size=guess_chance.sum())

    return np.clip(base, 0.7, 12.0)


def extract_features(times):
    hesitation_count = int(np.sum(times > 5))
    fast_answer_count = int(np.sum(times < 3))
    slow_answer_count = int(np.sum(times > 6))

    return {
        "avg_response_time": np.mean(times),
        "median_response_time": np.median(times),
        "max_response_time": np.max(times),
        "min_response_time": np.min(times),
        "std_response_time": np.std(times),
        "total_time": np.sum(times),
        "hesitation_count": hesitation_count,
        "hesitation_ratio": hesitation_count / len(times),
        "fast_answer_count": fast_answer_count,
        "slow_answer_count": slow_answer_count,
    }


def generate_synthetic_dataset(n_samples=1800, random_state=42):
    np.random.seed(random_state)
    rows = []

    labels = ["Impulsive", "Balanced", "Analytical"]

    for _ in range(n_samples):
        label = np.random.choice(labels, p=[0.34, 0.33, 0.33])
        times = generate_user_times(label)
        features = extract_features(times)

        # Label noise: real self-report / behavior labels are not perfect
        if np.random.rand() < 0.08:
            label = np.random.choice([x for x in labels if x != label])

        features["label"] = label
        rows.append(features)

    return pd.DataFrame(rows)


def train_model():
    df = generate_synthetic_dataset()
    df.to_csv(DATA_PATH, index=False)

    X = df.drop("label", axis=1)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=5,
        min_samples_leaf=8,
        random_state=42,
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    accuracy = accuracy_score(y_test, preds)
    cv_scores = cross_val_score(model, X, y, cv=5)

    print("Test Accuracy:", round(accuracy * 100, 2), "%")
    print("Cross-validation Accuracy:", round(cv_scores.mean() * 100, 2), "%")
    print()
    print("Classification Report:")
    print(classification_report(y_test, preds))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, preds))

    importance = pd.DataFrame({
        "feature": X.columns,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    print()
    print("Feature Importance:")
    print(importance)

    joblib.dump(model, MODEL_PATH)

    print()
    print("Dataset saved to:", DATA_PATH)
    print("Model saved to:", MODEL_PATH)


if __name__ == "__main__":
    train_model()
