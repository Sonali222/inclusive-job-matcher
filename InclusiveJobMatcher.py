import streamlit as st

st.set_page_config(page_title="Inclusive Job Matcher", layout="wide")

# --- Accessibility Settings Sidebar ---
st.sidebar.title("🔧 Settings")
font_size = st.sidebar.radio("Font Size", ["Small", "Medium", "Large"], index=1)
high_contrast = st.sidebar.checkbox("High Contrast Mode")

st.sidebar.markdown("---")

# --- Navigation Section ---
page = st.sidebar.radio("📂 Navigate to", [
    "🏠 Home",
    "🧩 User Profile",
    "🔍 Job Recommendations",
    "📄 Resume Generator"
])

# --- Accessibility Settings to session ---
st.session_state["accessibility"] = {
    "font_size": font_size,
    "high_contrast": high_contrast
}

# --- Apply Global Styling ---
font_px = {"Small": "14px", "Medium": "18px", "22px": "22px"}[font_size]
contrast_style = "color:white; background-color:black;" if high_contrast else ""
custom_style = f"<style>html, body, .stApp {{ font-size: {font_px}; {contrast_style} }}</style>"
st.markdown(custom_style, unsafe_allow_html=True)

# --- Route to Pages ---
if page.endswith("Home"):
    import home
    home.render_home()

elif page.endswith("User Profile"):
    import user_profile
    user_profile.render_user_profile()

elif page.endswith("Job Recommendations"):
    import recommendations
    recommendations.render_recommendations()

elif page.endswith("Resume Generator"):
    import resume_generator
    resume_generator.render_resume_generator()
