import streamlit as st


# Function to perform skill gap analysis
def skill_gap_analysis(user_skills, required_skills):
    user_skills_set = set(user_skills)
    required_skills_set = set(required_skills)

    # Find missing skills by subtracting user skills from required skills
    missing_skills = list(required_skills_set - user_skills_set)

    # Return the result
    return {
        "missing_skills": missing_skills,
        "user_skills": list(user_skills_set),
        "required_skills": list(required_skills_set),
    }


# Streamlit App Interface
st.title("Skill Gap Analysis for Job Seekers")

# Step 1: User Profile
st.subheader("1. User Profile")
user_name = st.text_input("Enter your name:")
profession = st.selectbox("Select your profession",
                          ["Software Engineer", "Data Scientist", "Web Developer", "Product Manager", "Other"])
experience_years = st.slider("Years of Experience", 0, 40, 2)

# Ensure user inputs profile information before proceeding
if user_name and profession and experience_years:
    # Step 2: Job Preferences
    st.subheader("2. Job Preferences")
    preferred_job_title = st.text_input("Preferred Job Title (e.g., Software Engineer, Data Scientist):",
                                        "Software Engineer")
    preferred_location = st.text_input("Preferred Location (e.g., San Francisco):", "San Francisco")

    if preferred_job_title and preferred_location:
        # Step 3: Required Skills (based on the selected job title)
        if preferred_job_title.lower() == "software engineer":
            required_skills = ["Python", "Machine Learning", "Flask", "API Development", "JavaScript"]
        elif preferred_job_title.lower() == "data scientist":
            required_skills = ["Python", "R", "Machine Learning", "SQL", "Deep Learning"]
        elif preferred_job_title.lower() == "web developer":
            required_skills = ["HTML", "CSS", "JavaScript", "React", "Node.js"]
        elif preferred_job_title.lower() == "product manager":
            required_skills = ["Project Management", "Communication", "Agile", "Leadership"]
        else:
            required_skills = ["Communication", "Project Management", "Leadership"]

        st.subheader("3. Enter Your Skills")
        user_skills_input = st.text_area("Enter your skills (comma-separated):", "")

        # Ensure user inputs their skills before proceeding
        if user_skills_input:
            # Convert the input string to a list of skills
            user_skills = [skill.strip() for skill in user_skills_input.split(",")]

            # Step 4: Perform Skill Gap Analysis
            result = skill_gap_analysis(user_skills, required_skills)

            # Display the result
            st.write("### Skill Gap Analysis Result:")
            st.write(f"*Your Name*: {user_name}")
            st.write(f"*Profession*: {profession}")
            st.write(f"*Experience*: {experience_years} years")
            st.write(f"*Preferred Job Title*: {preferred_job_title}")
            st.write(f"*Preferred Location*: {preferred_location}")
            st.write(f"*Required Skills*: {', '.join(result['required_skills'])}")
            st.write(f"*Your Skills*: {', '.join(result['user_skills'])}")

            if result['missing_skills']:
                st.write(f"### Missing Skills: {', '.join(result['missing_skills'])}")
            else:
                st.write("You have all the required skills for this job!")

# Instructions or information section
st.markdown("""
This app helps you analyze the skills you need for a job role by comparing your current skill set with a list of required skills for a particular job.

### How it works:
1. Fill in your *User Profile* (Name, Profession, Years of Experience).
2. Choose your *Job Preferences* (Job Title, Location).
3. Enter your *Skills* in the input box (separate them with commas).
4. The app will compare your skills with the required skills for the job role and show you any *missing skills*.

This is a simple way to understand if you're missing any essential skills for your dream job!
""")