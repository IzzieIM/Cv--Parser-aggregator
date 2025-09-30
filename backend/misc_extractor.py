# misc_extractor.py
def extract_headshot():
    # Placeholder: integrate with vision model (face detection in CV)
    return None

def extract_is_resume_probability(text: str):
    # Heuristic: CV length and presence of keywords
    keywords = ["education", "experience", "skills", "projects"]
    score = sum(1 for k in keywords if k in text.lower())
    return min(100, (score / len(keywords)) * 100)

def extract_redacted_text(text: str):
    if "xxxx" in text or "[redacted]" in text.lower():
        return True
    return False
