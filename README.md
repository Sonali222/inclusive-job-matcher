# Inclusive Job Matcher

## Project Overview
Finding jobs that truly consider accessibility needs is a challenge for many people with disabilities.  
This project bridges that gap by combining Large Language Models (Gemini), data engineering pipelines, and Streamlit to:

- Recommend jobs that align with a candidate’s skills, education, and accessibility requirements  
- Generate ATS-friendly resumes tailored to the top job postings  
- Provide an accessible and user-friendly interface  

---

## Problem Statement
- Traditional job boards do not highlight accessibility features in job postings  
- Applicants often spend hours tailoring resumes manually  
- Lack of centralized, DEI-focused platforms makes the job search harder for underrepresented communities  

---

## Solution
Our platform addresses these challenges by:

- Using **Gemini LLM** to filter and summarize job descriptions  
- Providing a **multi-page Streamlit application** for profile setup, job recommendations, and resume generation  
- Ensuring **built-in accessibility features** such as font size toggle, high contrast mode, and text-to-speech  
- Offering a **lightweight Application Tracker** for manual job application status logging  

---

## Architecture
The system is organized into the following layers:

1. **User Interface (Streamlit Frontend):** Home page, profile form, recommendations, and resume generator  
2. **Logic Layer (Gemini LLM):** Filters job postings and generates tailored resumes  
3. **Data Layer:** Accessible job dataset stored in Excel/CSV (future: database integration)  
4. **Application Tracker:** Records job application status using CSV or Google Sheets  

---

## Tech Stack
- **Frontend:** Streamlit  
- **Backend/Logic:** Python, Gemini LLM, LangChain  
- **Data:** Curated accessible job dataset (Excel/CSV)  
- **Infrastructure (Future):** AWS (Lambda, RDS, S3)  
- **Other Tools:** Pandas, GitHub for version control  

---

## Project Structure

```
folder/
├── file1.py
├── file2.py
```


## Getting Started

### 1. Create a Virtual Environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

### 2. Install Dependencies

```
pip install -r requirements.txt
```

## 3. Run the Application

```
streamlit run Home.py
```
## Future Enhancements 

- Integration with live job APIs (LinkedIn, Indeed, etc.)
- Deployment on AWS (Lambda, RDS, S3) or Streamlit Cloud
- Employer Inclusivity Score ranking system
- Cover letter generator powered by Gemini



