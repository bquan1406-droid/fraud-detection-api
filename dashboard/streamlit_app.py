import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="",
    layout="wide"
)

st.title("Credit Card Fraud Detection Dashboard")
st.markdown("Real-time fraud predictions using XGBoost model")

API_URL = "https://fraud-detection-api-231m.onrender.com/predict"

st.sidebar.header("Model Information")
st.sidebar.markdown("""
- Model: XGBoost
- Recall: 77.2%
- Precision: 39.9%
- F1 Score: 0.526
""")

st.sidebar.header("Threshold")
threshold = st.sidebar.slider("Fraud Threshold", 0.0, 1.0, 0.5929, 0.05)
st.sidebar.caption("Lower threshold = more fraud caught, more false alarms")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Test a Transaction")
    
    with st.form("prediction_form"):
        transaction_id = st.number_input("Transaction ID", value=12345, step=1)
        product_cd = st.selectbox("Product Code", ["W", "H", "C", "S", "R"])
        card1 = st.number_input("Card ID (card1)", value=13926, step=1)
        card4 = st.selectbox("Card Brand", ["visa", "mastercard", "american express", "discover"])
        transaction_amt = st.number_input("Transaction Amount ($)", value=68.50, step=10.0)
        addr1 = st.number_input("Address Code (addr1)", value=315.0, step=10.0)
        addr2 = st.number_input("Address Code (addr2)", value=87.0, step=10.0)
        transaction_dt = st.number_input("Transaction Time (DT)", value=86400, step=1000)
        
        submitted = st.form_submit_button("Predict Fraud")
        
        if submitted:
            payload = {
                "TransactionID": int(transaction_id),
                "ProductCD": product_cd,
                "card1": int(card1),
                "card4": card4,
                "TransactionAmt": float(transaction_amt),
                "addr1": float(addr1),
                "addr2": float(addr2),
                "TransactionDT": float(transaction_dt)
            }
            
            try:
                response = requests.post(API_URL, json=payload, timeout=30)
                result = response.json()
                
                fraud_prob = result.get("fraud_probability", 0)
                fraud_pred = result.get("fraud_prediction", 0)
                
                st.markdown("---")
                st.subheader("Result")
                
                if fraud_prob >= threshold:
                    st.error("FRAUD DETECTED")
                    st.metric("Fraud Probability", f"{fraud_prob*100:.1f}%")
                    st.caption(f"Alert sent: {result.get('alert_sent', False)}")
                else:
                    st.success("Transaction Approved")
                    st.metric("Fraud Probability", f"{fraud_prob*100:.1f}%")
                    st.caption(f"Alert sent: {result.get('alert_sent', False)}")
                    
            except Exception as e:
                st.error(f"API Error: {str(e)}")
                st.caption("Make sure the API is running")

with col2:
    st.subheader("Recent Alerts")
    st.info("This dashboard connects to your live fraud detection API")
    st.markdown("""
    How it works:
    1. Enter transaction details
    2. API sends data to XGBoost model
    3. Model returns fraud probability
    4. Alert sent if probability > threshold
    
    API Status:
    """)
    
    try:
        health_check = requests.get("https://fraud-detection-api-231m.onrender.com", timeout=10)
        if health_check.status_code == 200:
            st.success("API is online")
        else:
            st.warning("API returned unexpected status")
    except:
        st.error("API is offline or unreachable")

st.markdown("---")
st.caption("Fraud detection model trained on IEEE-CIS dataset. For demonstration purposes only.")
