# 🏥 Healthcare Policy Sales Agent

This is a Streamlit Cloud-deployable LLM-powered agent that recommends HealthSecure insurance policies.

## Deployment Steps on Streamlit Cloud

1. Push this folder to GitHub.
2. Go to https://share.streamlit.io/ and log in with GitHub.
3. Click "New App" and select this repository.
4. Set Branch: main, Main file: app.py
5. Add secret in Streamlit Cloud:
   Key: OPENAI_API_KEY
   Value: your OpenAI API key
6. Deploy and open the app URL.

## Usage

- Enter your age, family type, number of dependents, and any special requirements.
- Click "Get Policy Recommendations" to see suggested policies.
- Ask follow-up questions in the input field below.
