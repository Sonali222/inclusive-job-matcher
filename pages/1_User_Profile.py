import streamlit as st

st.title("🧩 Inclusive Job Matcher – User Profile")
st.markdown("Please complete the form below to receive personalized job recommendations.")

# Ensure session state is initialized
if "profile" not in st.session_state:
    st.session_state["profile"] = {}

profile = st.session_state["profile"]

with st.form("user_profile_form"):
    # Section 1: Personal Info
    name = st.text_input("1.1 Full Name", value=profile.get("name", ""))
    email = st.text_input("1.2 Email Address", value=profile.get("email", ""))
    phone = st.text_input("1.3 Phone Number (Optional)", value=profile.get("phone", ""))

    # Section 2: Disability Info
    st.markdown("### 2. Disability Information")
    disabilities = [
        "Physical Disability (e.g., wheelchair user, limb impairment)",
        "Vision Impairment (e.g., low vision, blindness)",
        "Hearing Impairment (e.g., hard of hearing, deaf)",
        "Cognitive or Learning Disability (e.g., dyslexia, ADHD)",
        "Mental Health Condition (e.g., anxiety, depression)",
        "Chronic Illness (e.g., arthritis, multiple sclerosis)",
        "Neurodivergent (e.g., autism spectrum, Asperger’s)",
        "Other"
    ]
    disability = st.multiselect("2.1 What type of disability do you have?", disabilities,
                                default=profile.get("disability", []))

    other_disability = ""
    if "Other" in disability:
        other_disability = st.text_input("2.1.a Please specify your disability:",
                                         value=profile.get("other_disability", ""))

    accommodations = st.multiselect("2.2 Do you require any workplace accommodations?", [
        "Wheelchair-accessible workspace",
        "Screen reader-friendly environment",
        "Sign language interpreter or captioning",
        "Flexible work hours",
        "Remote work options",
        "Ergonomic equipment",
        "Assistive technology (e.g., speech-to-text software)",
        "Other"
    ], default=profile.get("accommodations", []))

    # Section 3: Education & Skills
    st.markdown("### 3. Education & Skills")

    education_options = ["No formal education", "High School Diploma or GED", "Associate’s Degree",
                         "Bachelor’s Degree", "Master’s Degree or Higher", "Vocational Training/Certification"]
    education = st.selectbox("3.1 What is your highest level of education?", education_options,
                             index=education_options.index(profile.get("education", "High School Diploma or GED")))

    st.markdown("3.2 Select your skills from the categories below. You may select multiple per category:")
    technical_skills = ['Python', 'Java', 'SQL', 'Machine Learning', 'Data Analysis', 'Excel', 'Cloud Computing']
    soft_skills = ['Communication', 'Teamwork', 'Problem-Solving', 'Adaptability', 'Critical Thinking']
    industry_skills = ['Customer Service', 'Project Management', 'Sales', 'Healthcare IT', 'Retail']

    selected_technical = st.multiselect("Technical Skills", technical_skills, default=profile.get("selected_technical", []))
    selected_soft = st.multiselect("Soft Skills", soft_skills, default=profile.get("selected_soft", []))
    selected_industry = st.multiselect("Industry-Specific Skills", industry_skills, default=profile.get("selected_industry", []))

    custom_skills = st.text_input("Add any additional skills not listed above (comma-separated)",
                                  value=profile.get("custom_skills", ""))

    all_skills = selected_technical + selected_soft + selected_industry + \
                 [s.strip() for s in custom_skills.split(",") if s.strip()]

    # Section 4: Work Preferences
    st.markdown("### 4. Work Preferences")
    work_setup = st.multiselect("4.1 What type of work environment do you prefer?", [
        "Fully remote (Work from home)", "Hybrid (Mix of remote & in-office)",
        "In-office", "Open to any"
    ], default=profile.get("work_setup", []))

    schedule_options = ["Full-time (40+ hours/week)", "Part-time (Less than 30 hours/week)",
                        "Freelance / Contract", "Internship / Apprenticeship"]
    schedule = st.selectbox("4.2 What job schedule works best for you?", schedule_options,
                            index=schedule_options.index(profile.get("schedule", "Full-time (40+ hours/week)")))

    experience_levels = ["0–1 years", "1–3 years", "3–5 years", "5–7 years", "7+ years"]
    experience_level = st.selectbox("4.3 How much experience do you have?", experience_levels,
                                    index=experience_levels.index(profile.get("experience_level", "0–1 years")))

    preferred_role = st.text_input("4.4 Preferred Role (e.g., Software Engineer, Data Analyst, Cashier)",
                                   value=profile.get("preferred_role", ""))

    # Section 5: Resume/Recommendations
    st.markdown("### 5. Job Recommendations & Resume Assistance")
    want_resume = st.radio("5.1 Generate a personalized resume?", ["Yes", "No"],
                           index=["Yes", "No"].index(profile.get("want_resume", "Yes")))
    want_recommendations = st.radio("5.2 Get job recommendations?", ["Yes", "No"],
                                    index=["Yes", "No"].index(profile.get("want_recommendations", "Yes")))

    submit = st.form_submit_button("🔍 Get Job Matches")

# Validation and Save
if submit:
    validation_errors = []
    if not name.strip():
        validation_errors.append("Full Name is required.")
    if not email.strip() or "@" not in email:
        validation_errors.append("A valid Email Address is required.")
    if not disability:
        validation_errors.append("Please select at least one type of disability.")
    if not all_skills:
        validation_errors.append("Please select or enter at least one skill.")

    if validation_errors:
        st.warning("⚠️ Please fix the following issues before continuing:")
        for err in validation_errors:
            st.write(f"- {err}")
        st.stop()

    with st.spinner("Saving your profile and redirecting..."):
        st.session_state["profile"] = {
            "name": name,
            "email": email,
            "phone": phone,
            "disability": disability,
            "other_disability": other_disability,
            "accommodations": accommodations,
            "education": education,
            "selected_technical": selected_technical,
            "selected_soft": selected_soft,
            "selected_industry": selected_industry,
            "custom_skills": custom_skills,
            "skills": all_skills,
            "work_setup": work_setup,
            "schedule": schedule,
            "experience_level": experience_level,
            "preferred_role": preferred_role,
            "want_resume": want_resume,
            "want_recommendations": want_recommendations,
            "tts": st.session_state.get("tts", False)
        }

        st.success("✅ Profile saved!")

        # Optional skill preview
        st.markdown("### 🧠 Your Selected Skills")
        st.write(", ".join(all_skills) if all_skills else "No skills selected.")

        # Redirect logic
        if want_resume == "Yes":
            st.experimental_set_query_params(page="resume")
        elif want_recommendations == "Yes":
            st.experimental_set_query_params(page="recommendations")
        st.rerun()
