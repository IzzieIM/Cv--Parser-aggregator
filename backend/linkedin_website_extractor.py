# linkedin_websites_extractor.py
import re

def extract_linkedin(text: str):
    # Find all URLs in the text
    urls = re.findall(r"https?://[^\s]+", text)
    # Search for a URL containing 'linkedin.com'
    for url in urls:
        if "linkedin.com" in url.lower():
            return url
    return None

def extract_websites(text: str):
    return list(set(re.findall(r"https?://[^\s]+", text)))
