# objective_profession_summary_extractor.py
import re
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_objective(text: str):
    pattern = r"(Objective|Career Objective|Professional Summary)[:\- ]+(.*?)(?:\n\n|\Z)"
    m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return m.group(2).strip() if m else None

def extract_profession(text: str):
    pattern = r"\b(Engineer|Developer|Scientist|Manager|Consultant|Designer|Analyst|Specialist|Administrator|Coordinator)\b"
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(1).title() if m else None

def extract_summary(text: str):
    if len(text) < 200:
        return text
    result = summarizer(text[:1024], max_length=120, min_length=40, do_sample=False)
    return result[0]["summary_text"]
