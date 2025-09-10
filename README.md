# Inclusive Job Matcher

An AI-powered, accessibility-first job recommendation platform that helps people with disabilities find inclusive jobs and auto-generate tailored resumes.

## Table of Contents

1. [Project Overview](#project-overview)  
2. [Problem Statement](#problem-statement)  
3. [Solution](#solution)  
4. [Architecture](#architecture)  
5. [Tech Stack](#tech-stack)  
6. [Project Structure](#project-structure)  
7. [Getting Started](#getting-started)  
8. [Future Enhancements](#future-enhancements)  
9. [About the Author](#about-the-author)  

## Project Overview

Finding jobs that truly consider accessibility needs is a challenge for many people with disabilities.  
This project bridges that gap by combining Large Language Models (Gemini), data engineering pipelines, and Streamlit to:

- Recommend jobs that align with a candidate’s skills, education, and accessibility requirements  
- Generate ATS-friendly resumes tailored to the top job postings  
- Provide an accessible and user-friendly interface  

## Problem Statement

- Traditional job boards do not highlight accessibility features in job postings  
- Applicants often spend hours tailoring resumes manually  
- Lack of centralized, DEI-focused platforms makes the job search harder for underrepresented communities  

## Solution

Our platform addresses these challenges by:

- Using **Gemini LLM** to filter and summarize job descriptions  
- Providing a **multi-page Streamlit application** for profile entry, job recommendations, and resume generation  
- Ensuring **built-in accessibility features** such as font size toggle, high contrast mode, and text-to-speech  
- Offering a **lightweight Application Tracker** for manual job application status logging  

## Architecture

The system is organized into the following layers:

1. **User Interface (Streamlit Frontend)** – Home page, profile form, recommendations, and resume generator  
2. **AI Layer (Gemini LLM)** – Filters job postings and generates tailored resumes  
3. **Data Layer** – Accessible job dataset stored in Excel/CSV (future: database integration)  
4. **Application Tracker** – Records job application status using CSV or Google Sheets  

## Tech Stack

- **Frontend**: Streamlit  
- **Backend/Logic**: Python, Gemini LLM, LangChain  
- **Data**: Curated accessible job dataset (Excel/CSV)  
- **Infrastructure (future)**: AWS (Lambda, RDS, S3)  
- **Other Tools**: Pandas, GitHub for version control  

## Project Structure

```text
inclusive-job-matcher/
│
├── Home.py                # Intro page
├── 1_User_Profile.py      # Profile form
├── 2_Recommendations.py   # Recommendation logic
├── langchain_utils.py     # TTS and memory helpers
├── requirements.txt       # Dependencies
├── README.md              # Documentation
└── data/                  # Job dataset (ignored in git)


# Getting started



