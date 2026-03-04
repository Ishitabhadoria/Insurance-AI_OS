import streamlit as st
import pandas as pd
from brain import run_ai_os
import os
from openai import OpenAI

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.set_page_config(page_title="Insurance AI-OS", layout="wide")
st.title("Insurance Autonomous AI Operating System")

st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV or TXT", type=["csv", "txt"])

required_columns = ["claim_amount", "premium_amount", "region", "hospital"]

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_csv(uploaded_file, sep=",")
    st.success("File Uploaded Successfully")
else:
    st.warning("No file uploaded. Using default sample data.")

    data = pd.DataFrame({
        "claim_amount": [120000, 80000, 95000, 150000, 500000],
        "premium_amount": [30000, 25000, 27000, 35000, 40000],
        "region": ["Mumbai", "Delhi", "Bangalore", "Chennai", "Mumbai"],
        "hospital": ["Apollo", "Fortis", "Max", "Manipal", "Apollo"]
    })

missing_cols = [col for col in required_columns if col not in data.columns]
if missing_cols:
    st.error(f"Missing columns: {missing_cols}")
    st.stop()

st.subheader("Dataset Preview")
st.dataframe(data)

if st.button("Run Autonomous AI Scan"):

    risk, fraud, pricing, decision = run_ai_os(data)

    col1, col2, col3 = st.columns(3)

    col1.metric("Loss Ratio", risk["loss_ratio"])
    col2.metric("Fraud Probability", fraud["fraud_probability"])
    col3.metric("Suspicious Claims", fraud["suspicious_claims"])

    st.subheader("High Risk Region")
    st.write(risk["high_risk_region"])

    st.subheader("Flagged Hospital")
    st.write(fraud["top_flagged_hospital"])

    st.subheader("Pricing Suggestion")
    st.write(pricing["premium_adjustment"])

    st.subheader("AI Strategy Report")
    st.success(decision)

st.subheader("💬 Ask Question About Data (Offline Mode)")

user_question = st.text_input("Type your question here")

#if st.button("Ask AI"):
#    if question.strip() == "":
#        st.warning("Please enter a question.")
#    else:
#
#        data_summary = data.describe(include="all").to_string()
#
#        prompt = f"""
#        You are Insurance Data Analyst AI.
#
#        Dataset Summary:
#        {data_summary}
#
#        User Question:
#        {question}
#
#        Give clear business explanation.
#        """
#
#        response = client.chat.completions.create(
#            model="gpt-4o-mini",
#            messages=[{"role": "user", "content": prompt}]
#        )
#
#        st.success("AI Answer")
#        st.write(response.choices[0].message.content)
if st.button("Ask Question"):

    question = user_question.lower()

    if "total claim" in question:
        answer = f"Total Claim Amount is {data['claim_amount'].sum()}"

    elif "total premium" in question:
        answer = f"Total Premium Amount is {data['premium_amount'].sum()}"

    elif "loss ratio" in question:
        loss_ratio = data["claim_amount"].sum() / data["premium_amount"].sum()
        answer = f"Loss Ratio is {round(loss_ratio, 2)}"

    elif "high risk region" in question:
        region = data.groupby("region")["claim_amount"].sum().idxmax()
        answer = f"High Risk Region is {region}"

    elif "fraud probability" in question:
        avg = data["claim_amount"].mean()
        std = data["claim_amount"].std()
        z = (data["claim_amount"] - avg) / std
        suspicious = data[z > 1.5]
        fraud_prob = len(suspicious) / len(data)
        answer = f"Fraud Probability is {round(fraud_prob, 2)}"

    elif "suggest premium" in question:
        loss_ratio = data["claim_amount"].sum() / data["premium_amount"].sum()

        if loss_ratio > 0.75:
            answer = "Recommendation: Increase premium by 8%"
        elif loss_ratio < 0.4:
            answer = "Recommendation: Decrease premium by 5%"
        else:
            answer = "Recommendation: No change needed"

    else:
        answer = "Sorry, I cannot understand the question in offline mode."

    st.success(answer)
st.subheader("Claim Distribution by Region")
st.bar_chart(data.groupby("region")["claim_amount"].sum())

st.subheader("Premium vs Claim Comparison")
st.line_chart(data[["claim_amount", "premium_amount"]])