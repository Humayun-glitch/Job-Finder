import spacy
from PyPDF2 import PdfReader

def parse_cv(cv_path):
    nlp = spacy.load("en_core_web_sm")
    reader = PdfReader(cv_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ == "SKILL"]
    experience = [sent.text for sent in doc.sents if "experience" in sent.text.lower()]
    education = [sent.text for sent in doc.sents if "education" in sent.text.lower()]
    
    return {
        "skills": skills,
        "experience": experience,
        "education": education
    }