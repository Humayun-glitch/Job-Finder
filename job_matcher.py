from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup

def match_jobs(cv_details, job_listings):
    cv_text = " ".join(cv_details["skills"] + cv_details["experience"] + cv_details["education"])
    job_texts = [job["description"] for job in job_listings]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([cv_text] + job_texts)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    
    matched_jobs = []
    for i, similarity in enumerate(cosine_similarities):
        if similarity > 0.5:  # Threshold for matching
            matched_jobs.append(job_listings[i])
    
    return matched_jobs

def fetch_job_listings(desired_role, location="United States", limit=10):
    base_url = "https://www.indeed.com/jobs"
    params = {
        "q": desired_role,
        "l": location,
        "limit": limit
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        job_listings = []
        
        for job in soup.find_all("div", class_="job_seen_beacon"):
            title = job.find("h2", class_="jobTitle").text.strip()
            company = job.find("span", class_="companyName").text.strip()
            location = job.find("div", class_="companyLocation").text.strip()
            description = job.find("div", class_="job-snippet").text.strip()
            apply_link = "https://www.indeed.com" + job.find("a")["href"]
            
            job_listings.append({
                "title": title,
                "company": company,
                "location": location,
                "description": description,
                "apply_link": apply_link
            })
        
        return job_listings
    else:
        print(f"Failed to fetch job listings: {response.status_code}")
        return []