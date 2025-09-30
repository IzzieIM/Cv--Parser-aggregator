# certifications_extractor.py
import re

def extract_certifications(text: str):
    pattern = r"\b(Diploma|Certification|Certified|Course|Training|PGDAC|Certificate)\b.*"
    matches = re.findall(pattern, text, re.IGNORECASE)
    return list(set(matches)) if matches else None
