# publications_referees_extractor.py
import re

def extract_publications(text: str):
    pattern = r"(Publications|Research Papers|Articles)[:\- ]+(.*?)(?:\n\n|\Z)"
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    return [m[1].strip() for m in matches] if matches else None

def extract_referees(text: str):
    pattern = r"(References|Referees)[:\- ]+(.*?)(?:\n\n|\Z)"
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
    return [m[1].strip() for m in matches] if matches else []
