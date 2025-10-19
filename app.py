import streamlit as st
import fitz  # PyMuPDF
import os
import openai

st.set_page_config(page_title="Healthcare Policy Advisor", layout="wide")

st.title("🏥 Healthcare Policy Advisor")
st.markdown("### Get personalized health insurance recommendations based on your profile.")

# Load OpenAI API key from environment
openai.api_key = os.environ.get("OPENAI_API_KEY")

if not openai.api_key:
    st.error("⚠️ Please set your OPENAI_API_KEY in Streamlit Cloud secrets before using the app.")

# Load PDF policy text
@st.cache_data
def load_policy_text():
    with fitz.open("HealthSecure_Policies.pdf") as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

policy_text = load_policy_text()

# Sidebar inputs
st.sidebar.header("Enter Your Details")
age = st.sidebar.number_input("Age", min_value=0, max_value=100, value=30)
family_type = st.sidebar.selectbox("Coverage Type", ["Individual", "Family"])
dependents = st.sidebar.number_input("Number of Dependents", min_value=0, max_value=10, value=0)
special_reqs = st.sidebar.text_area("Special Requirements (e.g. dental, wellness, senior health)")

# Main logic
if st.sidebar.button("Get Policy Recommendations"):
    user_profile = f"""User details:
    - Age: {age}
    - Family Type: {family_type}
    - Dependents: {dependents}
    - Special Requirements: {special_reqs}
    """

    prompt = f"""You are a healthcare insurance sales assistant for HealthSecure Insurance Ltd.
    Based on the following policy document, recommend 1-2 suitable policies for the user.
    {user_profile}
    Policy Details:
    {policy_text[:8000]}"""

    with st.spinner("Analyzing policies..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful healthcare insurance policy assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=900
            )
            recommendation = response.choices[0].message.content
            st.subheader("🩺 Recommended Policy")
            st.write(recommendation)
        except Exception as e:
            st.error(f"Error calling OpenAI API: {e}")

# Follow-up questions
st.markdown("---")
user_followup = st.text_input("Ask another question about the policies:")
if user_followup and openai.api_key:
    followup_prompt = f"""Answer this query based on the following policy text only:
    {policy_text[:8000]}
    User question: {user_followup}"""
    try:
        followup_resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a healthcare policy assistant."},
                {"role": "user", "content": followup_prompt}
            ],
            temperature=0.5,
            max_tokens=700
        )
        st.markdown("### 💬 Response")
        st.write(followup_resp.choices[0].message.content)
    except Exception as e:
        st.error(f"Error calling OpenAI API: {e}")
