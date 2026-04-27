# Fraud Detection API

Real-time credit card fraud detection system using XGBoost. Catches 77% of fraudulent transactions with 40% precision.

# Demo
Fraud Detection API: https://fraud-detection-api-231m.onrender.com
Live Demo: https://fraud-detection-api.streamlit.app/

## Business Impact

- **77.2% recall** - Catches 3,190 out of 4,133 fraud attempts in validation
- **39.9% precision** - 4,805 false alarms per 118,108 transactions
- **F1 Score: 0.526** - Balanced for production use

For a typical bank where missed fraud costs 7x more than false positives, this trade-off is acceptable and deployable.

## Model Performance

| Metric | Value |
|--------|-------|
| Recall | 77.2% |
| Precision | 39.9% |
| F1 Score | 0.526 |
| AUC | 0.883 |

## Features

**23 engineered features:**
- Frequency encodings (card1, card4, ProductCD, addr1, addr2, card2, card3, email domains)
- Aggregation statistics (mean amount per card1, card2, addr1)
- Transaction amount split (dollars and cents)
- D column count
- Velocity features (time since last transaction)
- Email missing indicators and same domain indicator

**339 V columns** - Vesta engineered features

## Tech Stack

- XGBoost for classification
- FastAPI for real-time predictions
- Discord webhooks for alerts
- Streamlit for monitoring dashboard
- Render for deployment

## Repository Structure

fraud-detection-api/models/ - Trained model files (fraud_detection_xgboost.pkl, product_encoder.pkl, card4_encoder.pkl, feature_columns.pkl)
fraud-detection-api/src/ - FastAPI application
fraud-detection-api/dashboard/ - Streamlit dashboard
fraud-detection-api/tests/ - Unit tests
fraud-detection-api/requirements.txt - Python dependencies
fraud-detection-api/README.md - Documentation

## Quick Start

Clone the repository:
git clone https://github.com/YOUR_USERNAME/fraud-detection-api.git
cd fraud-detection-api

Install dependencies:
pip install -r requirements.txt

Run the API:
uvicorn src.app:app --reload

Test the API:
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"TransactionID": 12345, "ProductCD": "W", "card1": 13926, "card4": "visa", "TransactionAmt": 68.50, "addr1": 315, "addr2": 87, "TransactionDT": 86400}'

Expected response:
{"TransactionID": 12345, "fraud_prediction": 0, "fraud_probability": 0.23, "threshold": 0.5, "alert_sent": false}

## Training Process

The model was trained on the IEEE-CIS Fraud Detection dataset with 590,540 transactions, 3.5% fraud rate, and 394 raw columns.

Training steps:
1. Exploratory analysis of raw features
2. Feature engineering (23 derived features)
3. Hyperparameter tuning (max_depth grid search from 3 to 13)
4. XGBoost with scale_pos_weight=28 for class imbalance

Training notebook available on Kaggle.

## Future Improvements

- Add SHAP explanations for model interpretability
- Implement human-in-the-loop review queue
- Add A/B testing framework for model comparisons
- Real-time feature store with Redis
- MLflow for experiment tracking
- Add more aggregation features (email domain, address velocity)

## Author

Tran Bao Quan - Data Science Graduate (2026)

## License

MIT
