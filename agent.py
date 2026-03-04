import pandas as pd
import numpy as np
#from openai import OpenAI
#import os
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#
#def supervisor_llm(risk, fraud, pricing):
#
#    prompt = f"""
#    You are Chief Strategy AI of an insurance company.
#
#    Risk Analysis:
#    {risk}
#
#    Fraud Analysis:
#    {fraud}
#
#    Pricing Suggestion:
#    {pricing}
#
#    Provide:
#    1. Risk Interpretation
#    2. Fraud Insight
#    3. Strategic Business Recommendation
#    4. Urgency Level (Low/Medium/High)
#    """
#
#    response = client.chat.completions.create(
#        model="gpt-4o-mini",
#        messages=[{"role": "user", "content": prompt}]
#    )
#
#    return response.choices[0].message.content
def run_risk_agent(data):
    total_claims = data["claim_amount"].sum()
    total_premium = data["premium_amount"].sum()

    loss_ratio = total_claims / total_premium
    risk_score = min(loss_ratio, 1)

    high_risk_region = data.groupby("region")["claim_amount"].sum().idxmax()

    return {
        "total_claims": total_claims,
        "total_premium": total_premium,
        "loss_ratio": round(loss_ratio, 2),
        "risk_score": round(risk_score, 2),
        "high_risk_region": high_risk_region
    }

def run_fraud_agent(data):
    avg_claim = data["claim_amount"].mean()
    std_claim = data["claim_amount"].std()

    data["z_score"] = (data["claim_amount"] - avg_claim) / std_claim
    suspicious = data[data["z_score"] > 1.5]

    fraud_probability = min(len(suspicious) / len(data), 1)

    return {
        "fraud_probability": round(fraud_probability, 2),
        "suspicious_claims": len(suspicious),
        "top_flagged_hospital": suspicious["hospital"].mode()[0] if not suspicious.empty else "None"
    }

def run_pricing_agent(risk_output):
    if risk_output["loss_ratio"] > 0.75:
        return {"premium_adjustment": "Increase premium by 8%"}
    elif risk_output["loss_ratio"] < 0.4:
        return {"premium_adjustment": "Decrease premium by 5%"}
    else:
        return {"premium_adjustment": "No Change Recommended"}