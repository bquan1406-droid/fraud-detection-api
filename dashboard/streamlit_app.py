import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6c757d;
        margin-bottom: 2rem;
    }
    .result-box {
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #6c757d;
        margin-top: 0.5rem;
    }
    .fraud-alert {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    .approved-alert {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    .status-text {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }
    .probability-text {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .sidebar-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #667eea;
    }
    .info-box {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<div class="main-header">Fraud Detection System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Real-time credit card fraud detection using XGBoost</div>', unsafe_allow_html=True)

API_URL = "https://fraud-detection-api-231m.onrender.com/predict"
THRESHOLD = 0.5929

with st.sidebar:
    st.markdown('<div class="sidebar-header">Model Information</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">72%</div><div class="metric-label">Recall</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">50.5%</div><div class="metric-label">Precision</div></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">0.594</div><div class="metric-label">F1 Score</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{THRESHOLD}</div><div class="metric-label">Threshold</div></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### Model Architecture")
    st.markdown("- XGBoost Classifier")
    st.markdown("- 23 engineered features")
    st.markdown("- 339 Vesta V columns")
    st.markdown("- max_depth: 13")
    st.markdown("- learning_rate: 0.1")
    
    st.markdown("---")
    st.markdown("### Dataset")
    st.markdown("- IEEE-CIS Fraud Detection")
    st.markdown("- 590,540 transactions")
    st.markdown("- 3.5% fraud rate")

tab1, tab2, tab3 = st.tabs(["Test Transaction", "Methodology", "About"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Transaction Details")
        
        with st.form("prediction_form"):
            transaction_id = st.number_input("Transaction ID", value=999002, step=1)
            
            col_a, col_b = st.columns(2)
            with col_a:
                product_cd = st.selectbox("Product Code", ["W", "H", "C", "S", "R"])
                card1 = st.number_input("Card ID", value=2755, step=1)
                transaction_amt = st.number_input("Amount ($)", value=8900.00, step=100.0)
                addr1 = st.number_input("Address Code 1", value=476.0, step=10.0)
            with col_b:
                card4 = st.selectbox("Card Brand", ["visa", "mastercard", "american express", "discover"])
                transaction_dt = st.number_input("Time DT", value=86400, step=1000)
                addr2 = st.number_input("Address Code 2", value=87.0, step=10.0)
            
            submitted = st.form_submit_button("Predict Fraud", use_container_width=True)
            
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
                    st.markdown("### Prediction Result")
                    
                    if fraud_pred == 1:
                        st.markdown(f'''
                        <div class="fraud-alert">
                            <p class="status-text">FRAUD DETECTED</p>
                            <p class="probability-text">{fraud_prob*100:.1f}%</p>
                            <p class="status-text" style="font-size: 0.9rem;">Alert sent: {result.get('alert_sent', False)}</p>
                        </div>
                        ''', unsafe_allow_html=True)
                    else:
                        st.markdown(f'''
                        <div class="approved-alert">
                            <p class="status-text">Transaction Approved</p>
                            <p class="probability-text">{fraud_prob*100:.1f}%</p>
                            <p class="status-text" style="font-size: 0.9rem;">Risk probability</p>
                        </div>
                        ''', unsafe_allow_html=True)
                        
                except Exception as e:
                    st.error(f"API Error: {str(e)}")
    
    with col2:
        st.markdown("### System Status")
        
        try:
            health_check = requests.get("https://fraud-detection-api-231m.onrender.com", timeout=10)
            if health_check.status_code == 200:
                st.success("API is online")
            else:
                st.warning("API status unknown")
        except:
            st.error("API is offline")
        
        st.markdown("---")
        st.markdown("### Test Examples")
        
        with st.expander("Normal Transaction (Approved)"):
            st.code("""
Product Code: W
Card Brand: visa
Amount: $45.00
Address: 315, 87
            """)
        
        with st.expander("Fraud-like Transaction (Flagged)"):
            st.code("""
Product Code: C
Card Brand: discover
Amount: $8,900.00
Address: 476, 87
            """)
        
        with st.expander("High Risk Product Codes"):
            st.markdown("""
            - **Product C**: 11.7% fraud rate
            - **Product S**: 5.9% fraud rate
            - **Product H**: 4.8% fraud rate
            - **Product R**: 3.8% fraud rate
            - **Product W**: 2.0% fraud rate
            """)

with tab2:
    st.markdown("### Methodology")
    
    st.markdown("#### Feature Engineering (23 features)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Frequency Encodings**")
        st.markdown("- card1_freq, card4_freq, product_freq")
        st.markdown("- addr1_freq, addr2_freq")
        st.markdown("- card2_freq, card3_freq")
        st.markdown("- pemail_freq, remail_freq")
        st.markdown("- card1_card2_freq (interaction)")
    
    with col2:
        st.markdown("**Aggregation Statistics**")
        st.markdown("- card1_amt_mean, card1_amt_std")
        st.markdown("- card1_tx_count, card2_amt_mean")
        st.markdown("- addr1_amt_mean, addr1_tx_count")
        st.markdown("- amt_dollars, amt_cents")
        st.markdown("- d_count, same_email_domain")
    
    st.markdown("#### Model Training")
    st.markdown("""
    - **Algorithm:** XGBoost
    - **Hyperparameters:** max_depth=13, learning_rate=0.1, scale_pos_weight=28
    - **Train/Validation Split:** 80/20 with stratification
    - **Threshold Optimization:** Grid search to balance precision and recall
    - **Final Threshold:** 0.5929 achieving 72% recall, 50.5% precision
    """)
    
    st.markdown("#### Key Findings")
    st.markdown("""
    1. **ProductCD** is the strongest categorical predictor (fraud rate ranges from 2% to 11.7%)
    2. **Discover cards** show higher fraud rate (7.7%) than Visa (3.5%) or Mastercard (3.4%)
    3. **Fraud never exceeds $5,191** in the dataset (legitimate transactions go up to $31,937)
    4. **Email domain features** (missing indicators, frequency) add predictive power
    5. **Feature engineering** improved precision from 24% to 50% at similar recall
    """)

with tab3:
    st.markdown("### About This Project")
    
    st.markdown("""
    This fraud detection system was built as a portfolio project to demonstrate end-to-end machine learning deployment.
    
    **Dataset:** IEEE-CIS Fraud Detection dataset from Kaggle (590,540 transactions, 3.5% fraud rate)
    
    **Model:** XGBoost classifier with 23 engineered features + 339 Vesta V columns
    
    **Performance:** 72% recall, 50.5% precision at threshold 0.5929
    
    **Deployment:**
    - FastAPI backend on Render
    - Streamlit dashboard frontend
    - Discord webhook for real-time alerts
    
    **Business Impact:**
    For a bank processing 1 million transactions:
    - Catches 2,520 out of 3,500 actual fraud attempts (72%)
    - Creates 2,475 false alarms (2.5% of legitimate transactions)
    - Estimated savings: approximately $1.39M per 1M transactions
    
    **Technology Stack:**
    - Python, Pandas, NumPy
    - Scikit-learn, XGBoost
    - FastAPI, Streamlit
    - Render Cloud Platform
    """)
    
    st.markdown("---")
    st.markdown("### GitHub Repository")
    st.markdown("https://github.com/yourusername/fraud-detection-api")
    
    st.markdown("### Author")
    st.markdown("Tran Bao Quan - Data Science Graduate (2026)")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #6c757d; font-size: 0.8rem;'>Fraud detection model trained on IEEE-CIS dataset. For demonstration purposes only.</p>", unsafe_allow_html=True)
