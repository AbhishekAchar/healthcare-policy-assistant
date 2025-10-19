import streamlit as st
import fitz  # PyMuPDF
from openai import OpenAI
import os
st.set_page_config(page_title="Healthcare Policy Advisor", layout="wide")

st.title("🏥 Healthcare Policy Advisor")
st.markdown("### Get personalized health insurance recommendations based on your profile.")

# Initialize OpenAI client
client = OpenAI(api_key="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")
# Load and cache PDF policy text
@st.cache_data
def load_policy_text():
    with open("HealthSecure_Policies.pdf", "rb") as f:
        pdf = fitz.open(stream=f.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

policy_text = load_policy_text()

# Sidebar for user input
st.sidebar.header("Enter Your Details")
age = st.sidebar.number_input("Age", min_value=0, max_value=100, value=30)
family_type = st.sidebar.selectbox("Coverage Type", ["Individual", "Family"])
dependents = st.sidebar.number_input("Number of Dependents", min_value=0, max_value=10, value=0)
special_reqs = st.sidebar.text_area("Special Requirements (e.g. dental, wellness, senior health)")

if st.sidebar.button("Get Policy Recommendations"):
    query = f"""Suggest the most suitable health insurance policies based on:
    Age: {age}
    Family Type: {family_type}
    Dependents: {dependents}
    Special Requirements: {special_reqs}
    Refer only to the policy details provided below.
    Policy details:\n{policy_text[:8000]}"""  # limit text to fit token limits

    with st.spinner("Analyzing policies..."):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a healthcare insurance policy advisor."},
                {"role": "user", "content": query}
            ],
            max_tokens=400
        )
        recommendation = response.choices[0].message.content

    st.subheader("🩺 Recommended Policies")
    st.write(recommendation)

    st.markdown("---")
    st.markdown("💬 **Do you have more questions?** Type below to continue.")

    user_follow_up = st.text_input("Ask another question about the policies:")
    if user_follow_up:
        followup_query = f"""{user_follow_up}\nRefer only to this policy information:\n{policy_text[:8000]}"""
        followup_resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a healthcare policy assistant."},
                {"role": "user", "content": followup_query}
            ],
            max_tokens=400
        )
        st.write(followup_resp.choices[0].message.content)
