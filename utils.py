import os
from fpdf import FPDF
import webbrowser
import random

# Generate PDF Report
def generate_analysis_pdf(resume_text, roles, tips):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Resume Analysis Report", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt="Resume Text:\n" + resume_text)
    pdf.ln(5)

    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Suggested Job Roles", ln=True)
    pdf.set_font("Arial", size=10)
    for role in roles:
        pdf.cell(200, 8, txt=f"- {role}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Improvement Suggestions", ln=True)
    pdf.set_font("Arial", size=10)
    for tip in tips:
        pdf.multi_cell(0, 8, txt=f"- {tip}")

    output_path = os.path.join("resumes", "resume_analysis_report.pdf")
    pdf.output(output_path)
    return output_path

# Simulate chatbot feedback for tips
def get_chatbot_feedback(tip):
    responses = [
        f"That’s a great suggestion. Recruiters often look for this!",
        f"Yes, adding this can significantly improve visibility.",
        f"Good idea! It strengthens your overall profile.",
        f"That would definitely make your resume stand out."
    ]
    return random.choice(responses)

# Return dummy job board links
def get_job_search_links(role):
    query = role.replace(" ", "+")
    return {
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={query}",
        "Indeed": f"https://www.indeed.com/jobs?q={query}",
        "Naukri": f"https://www.naukri.com/{query}-jobs",
        "Monster": f"https://www.monster.com/jobs/search/?q={query}"
    }

# Resume chatbot (simple echo bot for now)
def chat_with_resume_bot(user_input, resume_text):
    keywords = ["skills", "experience", "projects", "certifications", "job"]
    if any(k in user_input.lower() for k in keywords):
        return "Make sure your resume includes strong details for that section."
    return "I recommend tailoring your resume to the job you're applying for."
