import joblib
import os

def load_model():
    if os.path.exists("model.pkl"):
        return joblib.load("model.pkl")
    return None

def predict(model, features):
    if model is None:
        return 1

    prob = model.predict_proba([features])[0][1]
    return 1 if prob > 0.6 else 0
