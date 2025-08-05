import streamlit as st
import pdfplumber
import os
from datetime import datetime
from role_predictor import suggest_roles
from resume_imporver import improve_resume
from utils import generate_analysis_pdf, get_chatbot_feedback, get_job_search_links

# Ensure directories exist
os.makedirs("resumes", exist_ok=True)
os.makedirs("data", exist_ok=True)

def save_uploaded_file(uploaded_file):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join("resumes", f"{timestamp}_{uploaded_file.name}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# Streamlit UI
st.set_page_config(page_title="Resume Analyzer", layout="wide")
st.title("📄 Resume Analyzer & Role Recommender")

uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

if uploaded_file:
    saved_path = save_uploaded_file(uploaded_file)
    st.success(f"✅ Resume uploaded: {os.path.basename(saved_path)}")

    resume_text = extract_text_from_pdf(saved_path)
    st.subheader("📑 Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=300)

    if st.button("🔍 Analyze Resume"):
        roles = suggest_roles(resume_text)[:2]
        tips = improve_resume(resume_text)

        st.subheader("💼 Suggested Job Roles")
        for role in roles:
            st.markdown(f"- **{role}**")

        st.subheader("🌐 Find Jobs Online")
        for role in roles:
            st.markdown(f"**🔍 Role:** {role}")
            for site, url in get_job_search_links(role).items():
                st.markdown(f"[{site}]({url})")

        st.subheader("📈 Resume Improvement Suggestions")
        for tip in tips:
            chatbot_reply = get_chatbot_feedback(tip)
            st.markdown(f"📌 **Suggestion**: {tip}")
            st.markdown(f"🤖 Chatbot: {chatbot_reply}")
       
      

        st.subheader("📤 Export Analysis")
        if st.button("📄 Download PDF Report"):
            pdf_path = generate_analysis_pdf(resume_text, roles, tips)
            with open(pdf_path, "rb") as f:
                st.download_button("⬇️ Download Report", f, file_name="resume_analysis.pdf")