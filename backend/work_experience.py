# work_experience_extractor.py
import re
import spacy

nlp = spacy.load("en_core_web_md")

def extract_total_experience(text: str):
    matches = re.findall(r"(\d+)\+?\s+(years|yrs)\s+of\s+experience", text, re.IGNORECASE)
    return max([int(m[0]) for m in matches], default=None) if matches else None

def extract_work_experience(text: str):
    doc = nlp(text)
    jobs = []
    for sent in doc.sents:
        if re.search(r"(experience|worked|employed|internship|position)", sent.text, re.I):
            jobs.append(sent.text.strip())
    return jobs if jobs else None
