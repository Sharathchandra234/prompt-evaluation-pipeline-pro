import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Prompt Evaluation Pipeline Pro", layout="wide")

st.title("🧠 Prompt Evaluation Pipeline Pro+")

st.markdown("Evaluate prompt quality, compare versions, and optimize AI instructions.")

# Inputs
st.subheader("📝 Evaluation Inputs")

question = st.text_area(
    "Task / Question",
    "Write a professional payment reminder email."
)

col1, col2 = st.columns(2)

with col1:
    prompt_a = st.text_area(
        "Prompt A",
        "Write a payment reminder email."
    )

with col2:
    prompt_b = st.text_area(
        "Prompt B",
        "Write a clear, professional, polite payment reminder email for a business customer."
    )

# Scoring Function
def score_prompt(prompt):
    p = prompt.lower()

    clarity = 20 if "clear" in p else 10
    tone = 20 if "professional" in p or "polite" in p else 10
    detail = 20 if len(prompt.split()) > 8 else 10
    structure = 20 if "," in prompt or "for" in p else 10
    specificity = 20 if "customer" in p or "business" in p else 10

    total = clarity + tone + detail + structure + specificity

    return {
        "Clarity": clarity,
        "Tone": tone,
        "Detail": detail,
        "Structure": structure,
        "Specificity": specificity,
        "Total": total
    }

# Evaluate
if st.button("🚀 Evaluate Prompts"):

    score_a = score_prompt(prompt_a)
    score_b = score_prompt(prompt_b)

    # KPI Cards
    c1, c2 = st.columns(2)
    c1.metric("Prompt A Total Score", score_a["Total"])
    c2.metric("Prompt B Total Score", score_b["Total"])

    st.markdown("---")

    # Comparison Table
    df = pd.DataFrame({
        "Metric": ["Clarity", "Tone", "Detail", "Structure", "Specificity", "Total"],
        "Prompt A": [
            score_a["Clarity"], score_a["Tone"], score_a["Detail"],
            score_a["Structure"], score_a["Specificity"], score_a["Total"]
        ],
        "Prompt B": [
            score_b["Clarity"], score_b["Tone"], score_b["Detail"],
            score_b["Structure"], score_b["Specificity"], score_b["Total"]
        ]
    })

    st.subheader("📋 Score Breakdown")
    st.dataframe(df, use_container_width=True)

    # Chart
    fig = px.bar(
        df[df["Metric"] != "Total"],
        x="Metric",
        y=["Prompt A", "Prompt B"],
        barmode="group",
        title="Prompt Comparison by Metric"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Winner
    st.markdown("---")

    if score_a["Total"] > score_b["Total"]:
        st.success("🏆 Prompt A is the better prompt.")
    elif score_b["Total"] > score_a["Total"]:
        st.success("🏆 Prompt B is the better prompt.")
    else:
        st.warning("🤝 Both prompts performed equally.")

    # Download Report
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Evaluation Report",
        csv,
        "prompt_evaluation_report.csv",
        "text/csv"
    )
