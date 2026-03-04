from agent import run_risk_agent, run_fraud_agent, run_pricing_agent


def supervisor_llm(risk, fraud, pricing):

    if risk["loss_ratio"] > 0.75:
        urgency = "High"
    elif fraud["fraud_probability"] > 0.3:
        urgency = "Medium"
    else:
        urgency = "Low"

    return f"""
    Risk Interpretation:
    Loss ratio is {risk['loss_ratio']} and high risk region is {risk['high_risk_region']}.

    Fraud Insight:
    Fraud probability is {fraud['fraud_probability']}.
    Suspicious claims count: {fraud['suspicious_claims']}.

    Strategic Business Recommendation:
    {pricing['premium_adjustment']}

    Urgency Level:
    {urgency}
    """
def run_ai_os(data):
    risk = run_risk_agent(data)
    fraud = run_fraud_agent(data)
    pricing = run_pricing_agent(risk)

    decision = supervisor_llm(risk, fraud, pricing)

    return risk, fraud, pricing, decision