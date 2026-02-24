# futuristic_shadow_ai.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Shadow AI – Behavioural Income Risk Engine",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Header
st.markdown("<h1 style='text-align:center;color:#1f77b4;'>Shadow AI – Behaviour Based Income Risk Engine</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;color:gray;'>Developed by Aditya Kumar | IIT Madras</h4>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar Inputs
st.sidebar.header("Customer Profile Inputs")
declared_income = st.sidebar.number_input("Declared Monthly Income (₹)", min_value=0, value=25000, step=1000)
bank_credits = st.sidebar.number_input("Average Monthly Bank Credits (₹)", min_value=0, value=40000, step=1000)
cash_deposit = st.sidebar.number_input("Average Monthly Cash Deposit (₹)", min_value=0, value=15000, step=500)
high_value_txn = st.sidebar.selectbox("High Value Transactions (Monthly)", ["Low", "Medium", "High"])
txn_count = st.sidebar.slider("Number of Transactions per Month", min_value=1, max_value=50, value=10)

# Risk Engine Calculation
estimated_income = bank_credits + cash_deposit
income_gap = estimated_income - declared_income

# Risk score 0-100
base_score = min(max(income_gap / declared_income * 100, 0), 100)
txn_modifier = {"Low": -5, "Medium": 0, "High": 10}[high_value_txn]
txn_count_modifier = min(txn_count, 50) / 5
risk_score = base_score + txn_modifier + txn_count_modifier
risk_score = min(max(risk_score, 0), 100)

# Risk Level & Color
if risk_score < 30:
    risk_level = "Low"
    color = "green"
elif risk_score < 60:
    risk_level = "Moderate"
    color = "orange"
else:
    risk_level = "High"
    color = "red"

# Display Results
st.subheader("Risk Analysis Results")
st.markdown(f"<h3>Estimated Income: ₹{estimated_income:,}</h3>", unsafe_allow_html=True)
st.markdown(f"<h3>Income Gap: ₹{income_gap:,}</h3>", unsafe_allow_html=True)
st.markdown(f"<h3>Behavioural Risk Score: <span style='color:{color};'>{risk_score:.2f} ({risk_level})</span></h3>", unsafe_allow_html=True)

# Visuals
st.subheader("Income & Transaction Overview")
df = pd.DataFrame({
    "Type": ["Declared Income", "Estimated Income", "Cash Deposit"],
    "Amount": [declared_income, estimated_income, cash_deposit]
})
st.bar_chart(df.set_index("Type"))

st.subheader("Transaction Distribution")
txn_df = pd.DataFrame({
    "Transaction Count": list(range(1, txn_count+1)),
    "Amount": [bank_credits/txn_count]*txn_count
})
st.line_chart(txn_df.set_index("Transaction Count"))

# Report download (CSV)
st.subheader("Download Risk Report")
report = pd.DataFrame({
    "Declared Income": [declared_income],
    "Estimated Income": [estimated_income],
    "Income Gap": [income_gap],
    "High Value Txn": [high_value_txn],
    "Transactions Count": [txn_count],
    "Risk Score": [risk_score],
    "Risk Level": [risk_level],
    "Generated At": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
})
st.download_button(
    label="Download CSV Report",
    data=report.to_csv(index=False),
    file_name="shadow_ai_risk_report.csv",
    mime="text/csv"
)

# Disclaimer
st.markdown("---")
st.info("This is a proof-of-concept prototype for internal demonstration only. Not for real credit decisions.")
