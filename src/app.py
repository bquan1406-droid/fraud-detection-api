from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.schemas import Transaction
from src.feature_engineering import load_frequency_dicts, engineer_features
import joblib
import pandas as pd
import numpy as np
import json

app = FastAPI(title="Fraud Detection API", description="Real-time credit card fraud detection", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://fraud-detection-api.streamlit.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('models/fraud_detection_final.pkl')
le_product = joblib.load('models/product_encoder.pkl')
le_card4 = joblib.load('models/card4_encoder.pkl')
feature_columns = joblib.load('models/feature_columns.pkl')

with open('models/threshold.json', 'r') as f:
    threshold_config = json.load(f)
THRESHOLD = threshold_config['threshold']

frequency_dicts = load_frequency_dicts()

@app.get("/")
def read_root():
    return {"message": "Fraud Detection API is running", "status": "active"}

@app.post("/predict")
def predict(transaction: Transaction):
    try:
        features_dict = engineer_features(transaction, frequency_dicts)
        
        features_dict['ProductCD_encoded'] = le_product.transform([transaction.ProductCD])[0]
        features_dict['card4_encoded'] = le_card4.transform([transaction.card4])[0]
        
        features_df = pd.DataFrame([features_dict])
        
        for col in feature_columns:
            if col not in features_df.columns:
                features_df[col] = 0
        features_df = features_df[feature_columns]
        
        proba = model.predict_proba(features_df)[0, 1]
        prediction = 1 if proba > THRESHOLD else 0
        
        return {
            "TransactionID": transaction.TransactionID,
            "fraud_prediction": prediction,
            "fraud_probability": round(proba, 4),
            "threshold": THRESHOLD,
            "alert_sent": prediction == 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
