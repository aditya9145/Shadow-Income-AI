import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shadow AI Income Engine")

st.title("Shadow AI – Behaviour Based Income Risk Engine")

declared_income = st.number_input("Declared Monthly Income (₹)", min_value=0)
monthly_credit = st.number_input("Average Monthly Bank Credits (₹)", min_value=0)
monthly_cash_deposit = st.number_input("Average Monthly Cash Deposit (₹)", min_value=0)
high_value_txn = st.number_input("High Value Transactions (>50k)", min_value=0)

if st.button("Run Analysis"):

    estimated_income = monthly_credit + (monthly_cash_deposit * 0.7)
    income_gap = estimated_income - declared_income

    risk_score = 0

    if income_gap > 50000:
        risk_score += 40

    if high_value_txn > 5:
        risk_score += 30

    if declared_income > 0:
        ratio = estimated_income / declared_income
        if ratio > 1.5:
            risk_score += 30

    st.write("### Result")
    st.write("Estimated Income:", estimated_income)
    st.write("Income Gap:", income_gap)
    st.write("Risk Score:", risk_score)

    if risk_score >= 60:
        st.error("High Risk")
    elif risk_score >= 30:
        st.warning("Moderate Risk")
    else:
        st.success("Low Risk")

    data = {
        "Declared": declared_income,
        "Estimated": estimated_income
    }

    st.bar_chart(data)
