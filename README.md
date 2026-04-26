# Fraud Detection API

Real-time credit card fraud detection system using XGBoost. Catches 77% of fraudulent transactions with 40% precision.

## Business Impact

- **77.2% recall** - Catches 3,190 out of 4,133 fraud attempts in validation
- **39.9% precision** - 4,805 false alarms per 118,108 transactions
- **F1 Score: 0.526** - Balanced for production use

For a typical bank where missed fraud costs 7x more than false positives, this trade-off is acceptable and deployable.

## Model Performance

| Metric | Value |
|--------|-------|
| Recall (fraud caught) | 77.2% |
| Precision | 39.9% |
| F1 Score | 0.526 |
| AUC | 0.883 |

## Features (23 engineered + 339 V columns)

**Frequency encodings:**
- card1_freq, card4_freq, product_freq
- addr1_freq, addr2_freq
- card2_freq, card3_freq
- pemail_freq, remail_freq
- card1_card2_freq (interaction)

**Aggregation statistics:**
- card1_amt_mean, card1_amt_std, card1_tx_count
- card2_amt_mean, addr1_amt_mean
- addr1_tx_count

**Derived features:**
- amt_dollars, amt_cents (split TransactionAmt)
- d_count (number of D columns populated)
- card1_last_tx_diff (velocity)
- P_email_missing, R_email_missing
- same_email_domain

**Raw features:**
- ProductCD, card4, TransactionAmt
- V1-V339 (Vesta engineered features)

## Tech Stack

| Component | Technology |
|-----------|------------|
| Model | XGBoost (max_depth=13, scale_pos_weight=28) |
| API | FastAPI |
| Monitoring | Streamlit |
| Alerts | Discord webhooks |
| Deployment | Render (free tier) |
| Language | Python 3.9+ |

## Repository Structure
fraud-detection-api/
├── models/
│ ├── fraud_detection_xgboost.pkl
│ ├── product_encoder.pkl
│ ├── card4_encoder.pkl
│ └── feature_columns.pkl
├── src/
│ ├── app.py
│ ├── feature_engineering.py
│ └── schemas.py
├── dashboard/
│ └── streamlit_app.py
├── tests/
│ ├── test_api.py
│ └── test_features.py
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md

## Quick Start

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/fraud-detection-api.git
cd fraud-detection-api
pip install -r requirements.txt
uvicorn src.app:app --reload
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "TransactionID": 12345,
    "ProductCD": "W",
    "card1": 13926,
    "card4": "visa",
    "TransactionAmt": 68.50,
    "addr1": 315,
    "addr2": 87,
    "TransactionDT": 86400
  }'
{
  "TransactionID": 12345,
  "fraud_prediction": 0,
  "fraud_probability": 0.23,
  "threshold": 0.5,
  "alert_sent": false
}
Training Process
The model was trained on the IEEE-CIS Fraud Detection dataset:

590,540 transactions

3.5% fraud rate (highly imbalanced)

394 raw columns

Training steps
Exploratory analysis of raw features

Feature engineering (23 derived features)

Hyperparameter tuning (max_depth grid search: 3 to 13)

XGBoost with scale_pos_weight=28 for class imbalance

Training notebook available on Kaggle.

Future Improvements
Add SHAP explanations for model interpretability

Implement human-in-the-loop review queue

Add A/B testing framework for model comparisons

Real-time feature store with Redis

MLflow for experiment tracking

Add more aggregation features (email domain, address velocity)

Author
Tran Bao Quan - Data Science Graduate (2026)
