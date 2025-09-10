import streamlit as st
import pandas as pd
import google.generativeai as genai
from langchain_utils import speak_text, add_to_memory
import re

st.title("🔍 Your AI-Powered Job Matches")

@st.cache_data
def load_data():
    return pd.read_excel("accessible_jobs_chicago_cursor.xlsx")

def build_prompt(profile, job_listings):
    user_info = f"""
Name: {profile['name']}
Disability: {', '.join(profile['disability'])}
Education: {profile['education']}
Skills: {profile['skills']}
Work Setup Preference: {profile['work_setup']}
Accommodations Needed: {', '.join(profile['accommodations'])}
Schedule: {profile['schedule']}
"""

    listings_text = "\n\n".join(
        f"Job Title: {row['Job Title']}\nCompany Info: {row.get('Company Info', 'N/A')}\nDescription: {row['Job Description']}\nLink: [Apply here]({row['Job Link']})"
        for _, row in job_listings.iterrows()
    )

    prompt = f"""
You are a job recommendation assistant that helps people with disabilities find inclusive, accessible, and meaningful employment opportunities based on their background and preferences.

Using the profile below, recommend real jobs that best match their skills, work setup preferences, schedule, and accommodation needs.

🔎 Core Principles:
- Prioritize **entry-level** or **trainable roles** unless the user's education and experience suggest readiness for more advanced positions.
- Tailor recommendations to align with the user's **listed disabilities and required accommodations**. Consider accessibility needs such as remote options, screen reader compatibility, or non-verbal communication.
- Avoid recommending jobs that inherently conflict with the user's accessibility requirements — unless the job explicitly includes accommodations.
- Respect the user's **preferred role** and **skillset**, but offer alternatives if a better match exists based on their profile.

💡 Matching Tips:
- If the user has technical skills (e.g., Python, SQL), suggest relevant **junior tech roles**.
- If the user has customer service skills, suggest **chat-based**, **remote**, or **inclusive support roles**.
- If the user has limited formal skills or education, suggest **trainable**, **entry-level**, or **supported employment** opportunities.

🛑 DO NOT:
- Make up job titles, companies, or links.
- Recommend inaccessible roles without clearly noted accommodations.

✅ DO:
- Use actual job listings provided below.
- Be thoughtful and inclusive in your reasoning.
- Provide variety but always justify why each job fits.

---

👤 User Profile:
{user_info}

🧾 Job Listings ({len(job_listings)} total):
{listings_text}

---

🎯 Return the **top 10 job matches** that best fit the user’s profile. For each job, include:
1. **Job Title + Company**
2. **Short Company Overview**
3. **Job Description Summary**
4. **Why this job is a good match** (focus on technical + accessibility fit)
5. **Application Link** using markdown `[Apply here](URL)`

---

💬 Then, include an **Interview Advice Card** with tips tailored to the user's background, disability, and role goals.
"""
    return prompt

# --- MAIN LOGIC ---
if "profile" not in st.session_state:
    st.warning("⚠️ Please complete your profile first.")
    st.stop()

profile = st.session_state["profile"]

if profile.get("want_recommendations", "Yes") == "No":
    st.info("ℹ️ You opted out of job recommendations.")
    st.stop()

# Text-to-Speech Toggle
tts_enabled = st.toggle("🔊 Enable Text-to-Speech", value=profile.get("tts", False))
profile["tts"] = tts_enabled
st.session_state["profile"] = profile

# Load and clean jobs
jobs_df = load_data()
jobs_df['Job Title'] = jobs_df['Job Title'].fillna("")
jobs_df['Job Description'] = jobs_df['Job Description'].fillna("")

# 🧼 Deduplicate by Job Title + Company Name
if "Company Name" in jobs_df.columns:
    jobs_df = jobs_df.drop_duplicates(subset=["Job Title", "Company Name"]).reset_index(drop=True)

# 🎓 Filter out jobs requiring degrees beyond user's qualification
education = profile.get("education", "").lower()
if any(level in education for level in ["high school", "secondary", "ged", "diploma", "associate"]):
    jobs_df = jobs_df[~jobs_df["Job Description"].str.lower().str.contains("bachelor|master")].reset_index(drop=True)


# Filter out senior-level jobs
senior_keywords = ["manager", "senior", "director", "vp", "lead"]
mask = ~jobs_df['Job Title'].str.contains('|'.join(senior_keywords), case=False, na=False)

# Convert skill list to lowercase string
skill_string = " ".join(profile.get("skills", [])).lower()

# Skill-based filtering logic
if any(word in skill_string for word in ["python", "java", "sql", "software", "developer", "engineer"]):
    keyword_filter = jobs_df['Job Title'].str.contains('software|developer|engineer', case=False, na=False)
    jobs_df = jobs_df[mask & keyword_filter]
elif "cashier" in profile["preferred_role"].lower() or any(skill in skill_string for skill in ["pos", "cash handling", "customer service"]):
    cashier_filter = jobs_df['Job Title'].str.contains('cashier|clerk|associate|grocery', case=False, na=False)
    jobs_df = jobs_df[mask & cashier_filter]
elif profile["disability"] and "vision" in profile["disability"][0].lower() and "remote" in [w.lower() for w in profile["work_setup"]]:
    if "customer service" in profile["preferred_role"].lower():
        filter_keywords = "customer|support|chat|accessibility|remote|assistive|reader"
    else:
        filter_keywords = "screen reader|qa|data entry|accessibility"
    vision_mask = jobs_df['Job Title'].str.contains(filter_keywords, case=False, na=False) | \
                  jobs_df['Job Description'].str.contains(filter_keywords, case=False, na=False)
    jobs_df = jobs_df[mask & vision_mask]
else:
    jobs_df = jobs_df[mask]

# Add relevance score based on skill matching
def compute_relevance(job_title, job_desc, profile_keywords):
    text = f"{job_title} {job_desc}".lower()
    return sum(1 for word in profile_keywords if word in text)

profile_keywords = skill_string.split()
jobs_df["RelevanceScore"] = jobs_df.apply(
    lambda row: compute_relevance(row["Job Title"], row["Job Description"], profile_keywords),
    axis=1
)
jobs_df = jobs_df.sort_values("RelevanceScore", ascending=False)

# Slider for number of jobs to pass to Gemini
job_limit = st.slider("How many jobs should I consider for matching?", min_value=10, max_value=100, step=10, value=50)
top_jobs = jobs_df.head(job_limit)
st.caption(f"📌 Considering {len(top_jobs)} jobs out of {len(jobs_df)} after filtering and ranking by relevance.")

# Run Gemini with hyperparameters
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
response = model.generate_content(
    build_prompt(profile, top_jobs),
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,
        top_k=40,
        top_p=0.85,
        max_output_tokens=2048
    )
).text
add_to_memory(profile["name"], response)

# Split response into job section + interview tips
split_match = re.split(r"(?=💬 Interview Advice Card)", response, maxsplit=1)
job_section = split_match[0].strip()
interview_section = split_match[1].strip() if len(split_match) > 1 else ""

st.session_state["job_recommendations"] = job_section

# Extract job matches for resume generation
job_matches = re.findall(r"### 📌 (.*?) at (.*?)\n\n\*\*Company Overview:\*\* (.*?)\n\n\*\*Job Description:\*\* (.*?)\n\n\*\*Why this is a good fit:\*\* (.*?)\n\n\*\*Application Link:\*\* \[Apply here\]\((.*?)\)", job_section, re.DOTALL)
st.session_state["job_matches"] = [
    {
        "Job Title": title,
        "Company": company,
        "Company Info": overview,
        "Job Description": desc,
        "Why Fit": why,
        "Job Link": link
    }
    for title, company, overview, desc, why, link in job_matches
]

# Feedback tracking
if "job_feedback" not in st.session_state:
    st.session_state["job_feedback"] = {}

if "applied_jobs" not in st.session_state:
    st.session_state["applied_jobs"] = []

# Render Job Cards with feedback + applied tracking
st.subheader("📄 Tailored Job Recommendations")
for i, block in enumerate(job_section.split("---")):
    block = block.strip()
    if block:
        st.markdown(f"""
        <div style="padding: 20px; margin-bottom: 20px; border-radius: 10px; background-color: #f9f9fb; border-left: 5px solid #4a90e2;">
        {block}
        </div>
        """, unsafe_allow_html=True)

        feedback = st.radio(f"🤔 Was this recommendation helpful?", ["👍 Yes", "👎 No", "Maybe"], key=f"feedback_{i}")
        st.session_state["job_feedback"][f"job_{i}"] = feedback

        if st.button(f"✅ Mark as Applied", key=f"applied_{i}"):
            st.session_state["applied_jobs"].append(f"job_{i}")
            st.success("Marked as applied!")

# Interview Advice Card
if interview_section:
    st.markdown("---")
    with st.expander("💬 Interview Advice Card", expanded=True):
        st.markdown(f"""
        <div style="padding: 16px; border-radius: 10px; background-color: #e6f4ff; border-left: 5px solid #3e8ef7;">
        {interview_section}
        </div>
        """, unsafe_allow_html=True)

if tts_enabled:
    speak_text(response)

