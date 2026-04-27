import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="",
    layout="wide"
)

st.title("Credit Card Fraud Detection Dashboard")
st.markdown("Real-time fraud predictions using XGBoost")

API_URL = "https://fraud-detection-api-231m.onrender.com/predict"
THRESHOLD = 0.5929

st.sidebar.header("Model Information")
st.sidebar.markdown(f"""
- **Model:** XGBoost
- **Threshold:** {THRESHOLD}
- **Recall:** 72.0%
- **Precision:** 50.5%
- **F1 Score:** 0.594
""")

tab1, tab2, tab3 = st.tabs(["Test Transaction", "About", "Methodology"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Transaction Details")
        
        with st.form("prediction_form"):
            transaction_id = st.number_input("Transaction ID", value=999002, step=1)
            product_cd = st.selectbox("Product Code", ["W", "H", "C", "S", "R"])
            card1 = st.number_input("Card ID (card1)", value=2755, step=1)
            card4 = st.selectbox("Card Brand", ["visa", "mastercard", "american express", "discover"])
            transaction_amt = st.number_input("Transaction Amount ($)", value=8900.00, step=100.0)
            addr1 = st.number_input("Address Code (addr1)", value=476.0, step=10.0)
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
                    
                    if fraud_pred == 1:
                        st.error("FRAUD DETECTED")
                        st.metric("Fraud Probability", f"{fraud_prob*100:.1f}%")
                        st.caption(f"Alert sent: {result.get('alert_sent', False)}")
                    else:
                        st.success("Transaction Approved")
                        st.metric("Fraud Probability", f"{fraud_prob*100:.1f}%")
                        st.caption(f"Alert sent: {result.get('alert_sent', False)}")
                        
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
    
    with col2:
        st.subheader("Model Status")
        try:
            health_check = requests.get("https://fraud-detection-api-231m.onrender.com", timeout=10)
            if health_check.status_code == 200:
                st.success("API is online")
            else:
                st.warning("API returned unexpected status")
        except:
            st.error("API is offline or unreachable")
        
        st.markdown("---")
        st.subheader("Test Transaction Examples")
        st.markdown("""
        **Normal Transaction (Should be approved):**
        - Product Code: W
        - Card Brand: visa
        - Amount: $45.00
        
        **Fraud-like Transaction (May be flagged):**
        - Product Code: C
        - Card Brand: discover
        - Amount: $8900.00
        """)

with tab2:
    st.header("About")
    st.markdown("""
    This fraud detection system uses machine learning to identify potentially fraudulent credit card transactions in real-time.
    
    **Dataset:** IEEE-CIS Fraud Detection dataset from Kaggle (590,540 transactions, 3.5% fraud rate)
    
    **Model:** XGBoost classifier with 23 engineered features + 339 Vesta V columns
    
    **Performance:** 72% recall, 50.5% precision at threshold 0.5929
    
    **API:** Deployed on Render, accessible via REST API
    
    **Alert System:** Discord webhook integration for real-time fraud alerts
    """)

with tab3:
    st.header("Methodology")
    
    st.subheader("Feature Engineering (23 features)")
    st.markdown("""
    **Frequency encodings:**
    - card1_freq, card4_freq, product_freq
    - addr1_freq, addr2_freq, card2_freq, card3_freq
    - pemail_freq, remail_freq
    - card1_card2_freq (interaction)
    
    **Aggregation statistics:**
    - card1_amt_mean, card1_amt_std, card1_tx_count
    - card2_amt_mean, addr1_amt_mean, addr1_tx_count
    
    **Derived features:**
    - amt_dollars, amt_cents (split TransactionAmt)
    - d_count (number of D columns populated)
    - P_email_missing, R_email_missing
    - same_email_domain
    """)
    
    st.subheader("Model Training")
    st.markdown("""
    - Algorithm: XGBoost
    - Hyperparameters: max_depth=13, learning_rate=0.1, scale_pos_weight=28
    - Train/validation split: 80/20 with stratification
    - Threshold optimization: 0.5929 achieving 72% recall, 50.5% precision
    """)
    
    st.subheader("Key Findings")
    st.markdown("""
    1. **ProductCD** is the strongest categorical predictor (fraud rate ranges from 2% to 11.7%)
    2. **Discover cards** show higher fraud rate (7.7%) than other brands
    3. **Transaction amount** alone is weak, but combined with other features becomes useful
    4. **Email domain features** (missing indicators, frequency) add predictive power
    5. **Feature engineering** improved precision from 24% to 50% at similar recall
    """)
    
    st.subheader("Business Impact")
    st.markdown("""
    For a bank processing 1 million transactions:
    - Catches 2,520 out of 3,500 actual fraud attempts (72%)
    - Creates 2,475 false alarms (2.5% of legitimate transactions)
    - Based on industry cost estimates ($1,200 per missed fraud, $180 per false alarm):
      - Savings: approximately $1.39M per 1M transactions
    
    The model prioritizes catching fraud over avoiding false alarms, which aligns with bank priorities where missed fraud costs significantly more than false positives.
    """)

st.markdown("---")
st.caption("Fraud detection model trained on IEEE-CIS dataset. For demonstration purposes only.")
