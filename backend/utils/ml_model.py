import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
import joblib

model_path = "models/portfolio_model.pkl"

def train_model():
    np.random.seed(42)
    data = pd.DataFrame({
        "Buy Price": np.random.uniform(100, 500, 300),
        "Current Price": np.random.uniform(100, 500, 300),
        "Quantity": np.random.randint(1, 100, 300)
    })
    data["Gain"] = (data["Current Price"] - data["Buy Price"]) / data["Buy Price"]
    data["Target"] = (data["Gain"] > 0.10).astype(int)

    X = data[["Buy Price", "Current Price", "Quantity"]]
    y = data["Target"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    return model

try:
    model = joblib.load(model_path)
except Exception:
    model = train_model()

def generate_recommendations(portfolio_df):
    features = portfolio_df[['Buy Price', 'Current Price', 'Quantity']]
    preds = model.predict(features)
    probs = model.predict_proba(features)

    recommendations = []
    for i, stock in enumerate(portfolio_df['Stock']):
        label = preds[i]
        confidence = max(probs[i]) * 100
        recommendations.append({
            "stock": stock,
            "action": "Buy" if label == 1 else "Sell",
            "confidence": round(confidence, 2)
        })

    return recommendations