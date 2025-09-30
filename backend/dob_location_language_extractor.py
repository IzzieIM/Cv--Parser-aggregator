# dob_location_language_extractor.py
import re
import spacy

nlp = spacy.load("en_core_web_md")

def extract_dob(text: str):
    # Common DOB patterns
    dob_patterns = [
        r"(?:DOB|Date of Birth)[:\- ]+(\d{1,2}[\/\-\.\s]\d{1,2}[\/\-\.\s]\d{2,4})",
        r"(?:DOB|Date of Birth)[:\- ]+([A-Za-z]+\s\d{1,2},\s\d{4})"
    ]
    for pat in dob_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None

# ...existing code...
def extract_location(text: str):
    doc = nlp(text)
    # Try to find explicit "Location:" or "Address:" lines first
    explicit = []
    for line in text.splitlines():
        if re.search(r"(Location|Address)[:\-]", line, re.I):
            loc = re.sub(r"(Location|Address)[:\-]\s*", "", line, flags=re.I).strip()
            if loc:
                explicit.append(loc)
    if explicit:
        return explicit[0]  # Return the first explicit location found

    # Otherwise, use NER but filter out likely garbage
    locs = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
    # Remove locations that are part of education or company names
    filtered = []
    edu_keywords = ["university", "college", "institute", "school", "academy", "iit", "nit"]
    for loc in locs:
        if not any(kw in loc.lower() for kw in edu_keywords):
            filtered.append(loc)
    return filtered[0] if filtered else None
# ...existing code...

def extract_languages(text: str):
    langs = re.findall(r"\b(English|Hindi|Marathi|French|German|Spanish|Chinese|Japanese)\b", text, re.IGNORECASE)
    return list(set(langs)) if langs else None
