import streamlit as st
import pandas as pd
import google.generativeai as genai
from fpdf import FPDF
from langchain_utils import speak_text

st.title("📄 Personalized Resume Generator")

# ✅ Check preconditions
if "profile" not in st.session_state or "job_matches" not in st.session_state:
    st.warning("⚠️ Please complete your profile and view job recommendations first.")
    st.stop()

profile = st.session_state["profile"]
job_matches = st.session_state["job_matches"]

# ✅ Function to sanitize text for PDF (remove unsupported unicode)
def sanitize_for_pdf(text):
    replacements = {
        '–': '-',  # en dash
        '—': '-',  # em dash
        '“': '"', '”': '"',  # smart quotes
        '‘': "'", '’': "'",  # smart apostrophes
        '•': '-',  # bullet point
        '…': '...',  # ellipsis
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

# ✅ Resume Form
st.markdown("### ✏️ Please provide more details for resume tailoring:")
with st.form("resume_form"):
    education = st.text_area("🎓 Education (e.g., Degree, School, Years)", "")
    experience = st.text_area("💼 Past Work Experience (bullets or summary)", "")
    certifications = st.text_area("📜 Certifications (Optional)", "")
    projects = st.text_area("🛠️ Projects (Optional)", "")
    linkedin = st.text_input("🔗 LinkedIn Profile URL (Optional)", "")
    summary = st.text_area("🧠 Professional Summary (Optional)", "")

    submit = st.form_submit_button("🪄 Generate Resume")

# ✅ Generate Gemini-Powered Resume
if submit:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    jobs_text = "\n\n".join([
        f"- {job['Job Title']} at {job['Company']}\n  Description: {job['Job Description']}"
        for job in job_matches
    ])

    resume_prompt = f"""
You are a resume writer. Based on the user's info and the job descriptions, write an ATS-friendly professional resume in plain text with clean formatting.

USER INFO:
Name: {profile['name']}
Email: {profile['email']}
Phone: {profile['phone']}
Disability: {', '.join(profile['disability'])}
Education: {education}
Experience: {experience}
Skills: {profile['skills']}
Certifications: {certifications}
Projects: {projects}
LinkedIn: {linkedin}
Summary: {summary}

MATCHED JOBS:
{jobs_text}

Format:
- Start with name and contact
- Summary section (if given)
- Skills (bullets or comma-separated)
- Education
- Work Experience (tailored to job descriptions)
- Certifications and Projects (optional)
Keep resume under 1 page. Use concise bullet points. Avoid repetition. Return clean plain text only.
"""

    response = model.generate_content(resume_prompt).text
    st.success("✅ Resume generated successfully!")

    # Display resume preview
    st.text_area("🧾 Preview Resume", response, height=400)

    # Convert to PDF with sanitized text
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    pdf.set_font("Arial", size=10)

    for line in sanitize_for_pdf(response).split("\n"):
        pdf.multi_cell(0, 7, line)

    pdf_output = f"{profile['name'].replace(' ', '_')}_resume.pdf"
    pdf.output(pdf_output)

    with open(pdf_output, "rb") as file:
        st.download_button(
            label="📥 Download Resume as PDF",
            data=file,
            file_name=pdf_output,
            mime="application/pdf"
        )
