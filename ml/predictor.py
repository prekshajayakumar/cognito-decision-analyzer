import os
import joblib
import numpy as np


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "decision_model.pkl")


FEATURE_ORDER = [
    "avg_response_time",
    "median_response_time",
    "max_response_time",
    "min_response_time",
    "std_response_time",
    "total_time",
    "hesitation_count",
    "hesitation_ratio",
    "fast_answer_count",
    "slow_answer_count",
]


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("ML model not found. Run: python ml/train_model.py")
    return joblib.load(MODEL_PATH)


def predict_decision_style(features):
    model = load_model()

    X = np.array([[features[name] for name in FEATURE_ORDER]])

    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    confidence = float(max(probabilities))

    return prediction, round(confidence * 100, 2)
