import streamlit as st
import pdfplumber
import os
from datetime import datetime
from role_predictor import suggest_roles
from resume_imporver import improve_resume
from utils import generate_analysis_pdf, get_chatbot_feedback, get_job_search_links, chat_with_resume_bot

# Ensure directories exist
os.makedirs("resumes", exist_ok=True)
os.makedirs("data", exist_ok=True)

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# Title section
st.markdown("<h1 style='text-align: center;'>📄 Smart Resume Analyzer & Role Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload your resume and get tailored job suggestions, resume tips, and job links!</p>", unsafe_allow_html=True)

# Upload file
uploaded_file = st.file_uploader("📤 Upload Your Resume (PDF only)", type=["pdf"])

# Save file
def save_uploaded_file(uploaded_file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("resumes", f"{timestamp}_{uploaded_file.name}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

# Extract PDF
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)
    st.success("✅ Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(file_path)

    with st.expander("📑 View Extracted Resume Text"):
        st.text_area("Extracted Text", resume_text, height=250)

    if st.button("🔍 Analyze Resume"):
        roles = suggest_roles(resume_text)
        tips = improve_resume(resume_text)

        st.markdown("## 💼 Suggested Job Roles")
        cols = st.columns(3)
        for i, role in enumerate(roles):
            with cols[i % 3]:
                st.success(f"🎯 {role}")

        st.markdown("## 🌐 Job Search Links")
        for role in roles:
            with st.expander(f"🔍 Search for **{role}** jobs"):
                job_links = get_job_search_links(role)
                for site, url in job_links.items():
                    st.markdown(f"- [{site}]({url})")

        st.markdown("## 📈 Resume Improvement Suggestions")
        for tip in tips:
            chatbot_reply = get_chatbot_feedback(tip)
            st.markdown(f"📌 **Tip:** {tip}")
            st.markdown(f"🤖 **Bot:** _{chatbot_reply}_")

        # Download PDF
        if st.button("📄 Download PDF Report"):
            pdf_path = generate_analysis_pdf(resume_text, roles, tips)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download Report", f, file_name="resume_analysis.pdf")

        # Chatbot interface
        st.markdown("## 💬 Ask the Resume Chatbot")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_question = st.text_input("Type your resume or career question:")
        if st.button("Send"):
            if user_question:
                bot_answer = chat_with_resume_bot(user_question, resume_text)
                st.session_state.chat_history.append(("You", user_question))
                st.session_state.chat_history.append(("Bot", bot_answer))

        for speaker, msg in st.session_state.chat_history:
            st.markdown(f"**{speaker}:** {msg}")

# Footer / Feedback
st.markdown("---")
st.markdown("### 🙋 Feedback")
feedback = st.text_input("Do you have any suggestions or issues?")
if st.button("Submit Feedback"):
    st.success("✅ Thank you! We'll use your feedback to improve the app.")
