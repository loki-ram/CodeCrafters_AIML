
import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import fitz  # PyMuPDF (for PDF parsing)
import docx  # For docx parsing
from io import BytesIO
import re
from PyPDF2 import PdfReader

def skill_gap_analysis_app():
    def skill_gap_analysis(user_skills, required_skills, resume_text, job_keywords):
    # Extract the missing skills based on the job description and user resume
    all_skills = list(set(user_skills + required_skills))
    user_vector = [1 if skill in user_skills else 0 for skill in all_skills]
    required_vector = [1 if skill in required_skills else 0 for skill in all_skills]
    user_vector = np.array(user_vector).reshape(1, -1)
    required_vector = np.array(required_vector).reshape(1, -1)
    cosine_sim = cosine_similarity(user_vector, required_vector)[0][0]

    # Skill Gap Analysis
    missing_skills = [skill for skill in required_skills if skill not in user_skills]

    # ATS Keyword Match
    matched_keywords, match_percentage = match_keywords(resume_text, job_keywords)

    return {
        "missing_skills": missing_skills,
        "user_skills": list(set(user_skills)),
        "required_skills": list(set(required_skills)),
        "cosine_similarity": cosine_sim,
        "ats_score": match_percentage,
        "matched_keywords": matched_keywords
    }


# Function to extract text from PDF resume
def extract_skills_from_pdf(uploaded_file):
    # Read the uploaded file's byte stream
    pdf_bytes = uploaded_file.read()
    # Open the PDF directly from the byte stream
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


# Function to extract text from DOCX resume
def extract_skills_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text


# Function to extract skills from the text
def extract_skills_from_text(text):
    skills = ["Python", "Machine Learning", "Flask", "API Development", "JavaScript", "R",
              "Deep Learning", "Data Visualization", "SQL", "HTML", "CSS", "React", "Node.js",
              "Project Management", "Agile", "Leadership", "Communication", "User Research",
              "Wireframing", "Prototyping", "Figma", "Adobe XD"]
    text = text.lower()
    extracted_skills = [skill for skill in skills if skill.lower() in text]
    return extracted_skills


# Function to check for keyword match
def match_keywords(resume_text, job_keywords):
    matched_keywords = [kw for kw in job_keywords if kw.lower() in resume_text.lower()]
    match_percentage = (len(matched_keywords) / len(job_keywords)) * 100
    return matched_keywords, match_percentage


# Coursera links based on skills
coursera_links = {
    "Python": "https://www.coursera.org/courses?query=python",
    "Machine Learning": "https://www.coursera.org/courses?query=machine%20learning",
    "Flask": "https://www.coursera.org/courses?query=flask",
    "API Development": "https://www.coursera.org/courses?query=api%20development",
    "JavaScript": "https://www.coursera.org/courses?query=javascript",
    "R": "https://www.coursera.org/courses?query=r",
    "Deep Learning": "https://www.coursera.org/courses?query=deep%20learning",
    "Data Visualization": "https://www.coursera.org/courses?query=data%20visualization",
    "SQL": "https://www.coursera.org/courses?query=sql",
    "HTML": "https://www.coursera.org/courses?query=html",
    "CSS": "https://www.coursera.org/courses?query=css",
    "React": "https://www.coursera.org/courses?query=react",
    "Node.js": "https://www.coursera.org/courses?query=node.js",
    "Project Management": "https://www.coursera.org/courses?query=project%20management",
    "Agile": "https://www.coursera.org/courses?query=agile",
    "Leadership": "https://www.coursera.org/courses?query=leadership",
    "Communication": "https://www.coursera.org/courses?query=communication",
    "User Research": "https://www.coursera.org/courses?query=user%20research",
    "Wireframing": "https://www.coursera.org/courses?query=wireframing",
    "Prototyping": "https://www.coursera.org/courses?query=prototyping",
    "Figma": "https://www.coursera.org/courses?query=figma",
    "Adobe XD": "https://www.coursera.org/courses?query=adobe%20xd",
}

# Load the dataset containing job titles and required skills
job_skill_data = pd.read_csv(r"C:\Users\Dell\Documents\project\expanded_jobs_vs_skills.csv")

# Streamlit App Interface
st.title("Skill Gap Analysis for Job Seekers")

# Step 1: User Profile
st.subheader("1. User Profile")
user_name = st.text_input("Enter your name:")
profession = st.selectbox("Select your profession",
                          ["Software Engineer", "Data Scientist", "Web Developer", "Product Manager",
                           "UX/UI Designer", "Business Analyst", "Marketing Manager", "Data Analyst", "Other"])

experience_years = st.slider("Years of Experience", 0, 40, 2)

# Step 2: Upload Resume
st.subheader("2. Upload Your Resume (PDF/DOCX)")
uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])

# Step 3: Extract Skills from Resume if file is uploaded
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        resume_text = extract_skills_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        resume_text = extract_skills_from_docx(uploaded_file)

    user_skills = extract_skills_from_text(resume_text)
    st.write(f"Extracted Skills from Resume: {', '.join(user_skills)}")
else:
    user_skills_input = st.text_area("Enter your skills (comma-separated):", "")
    user_skills = [skill.strip() for skill in user_skills_input.split(",")] if user_skills_input else []

# Ensure user inputs profile information before proceeding
if user_name and profession and experience_years and user_skills:
    # Step 4: Job Preferences
    st.subheader("3. Job Preferences")
    preferred_job_title = st.text_input("Preferred Job Title (e.g., Software Engineer, Data Scientist):",
                                        "Software Engineer")
    preferred_location = st.text_input("Preferred Location (e.g., San Francisco):", "San Francisco")

    company_type = st.selectbox("Preferred Company Type",
                                ["Startups", "Large Corporations", "Non-Profit", "Freelance", "Remote", "Any"])

    if preferred_job_title and preferred_location:
        # Step 5: Required Skills (based on the selected job title)

        job_row = job_skill_data[job_skill_data['Job Title'].str.lower() == preferred_job_title.lower()]

        if not job_row.empty:
            required_skills = job_row['Skills Required'].iloc[0].split(",")  # Splitting skills by comma
            required_skills = [skill.strip() for skill in required_skills]  # Clean up extra spaces
        else:
            required_skills = ["Communication", "Project Management", "Leadership"]

        st.subheader("4. Skill Gap Analysis")
        # Perform Skill Gap Analysis using Cosine Similarity and ATS Score
        result = skill_gap_analysis(user_skills, required_skills, resume_text,
                                    ["Python", "Data Analysis", "Machine Learning", "NLP",
                                     "Deep Learning", "SQL", "API Development", "Team Collaboration"])

        # Display the result
        st.write("### Skill Gap Analysis Result:")
        st.write(f"*Your Name*: {user_name}")
        st.write(f"*Profession*: {profession}")
        st.write(f"*Experience*: {experience_years} years")
        st.write(f"*Preferred Job Title*: {preferred_job_title}")
        st.write(f"*Preferred Location*: {preferred_location}")
        st.write(f"*Preferred Company Type*: {company_type}")
        st.write(f"*Required Skills*: {', '.join(result['required_skills'])}")
        st.write(f"*Your Skills*: {', '.join(result['user_skills'])}")
        st.write(f"*Cosine Similarity Score*: {result['cosine_similarity'] * 100:.2f}%")
        st.write(f"*ATS Match Percentage*: {result['ats_score']:.2f}%")

        if result['missing_skills']:
            st.write(f"### Missing Skills: {', '.join(result['missing_skills'])}")
            st.write("To improve your skills, consider taking the following courses on Coursera:")
            for missing_skill in result['missing_skills']:
                coursera_url = coursera_links.get(missing_skill, "https://www.coursera.org")
                st.write(f"- [{missing_skill} Courses]({coursera_url})")
        else:
            st.write("You have all the required skills for this job!")