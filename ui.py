import streamlit as st
from cv_parser import parse_cv
from job_matcher import fetch_job_listings
from job_matcher import match_jobs


st.title("AI Job Finder")
uploaded_file = st.file_uploader("Upload your CV", type="pdf")
desired_role = st.text_input("Enter your desired role")

if uploaded_file and desired_role:
    cv_details = parse_cv(uploaded_file)
    job_listings = fetch_job_listings(desired_role)
    matched_jobs = match_jobs(cv_details, job_listings)
 #   suggestions = get_improvement_suggestions(cv_details, desired_role)
    
    st.write("### Matched Jobs")
    for job in matched_jobs:
        st.write(f"**{job['title']}** at {job['company']}")
        st.write(f"**Location**: {job['location']}")
        st.write(f"**Apply Here**: {job['apply_link']}")
    
#     st.write("### Improvement Suggestions")
#     for suggestion in suggestions:
#         st.write(suggestion)
else:
    st.write("Please upload your CV and enter your desired role.")