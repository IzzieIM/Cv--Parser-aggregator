# 📄 CV--Parser-aggregator

An NLP-powered CV/Resume parser that extracts structured information such as **name, email, education, work experience, past companies, contact number, projects**, and more. This project leverages **pretrained transformer models (NER)** + **regex-based extraction** to convert unstructured CV text into machine-readable JSON.

---

## ✨ Features

* 🔍 Extracts candidate details:

  * Name
  * Email(s)
  * Contact number(s)
  * LinkedIn / Portfolio links
* 🎓 Education details (schools, colleges, degrees, GPA/CGPA/percentages)
* 💼 Work experience (roles, duration, responsibilities)
* 🏢 Past companies (NER-based extraction)
* 💡 Projects (academic & personal)
* 📑 Additional metadata like skills, languages, and certifications

---

## 🛠️ Tech Stack

* **Python 3.9+**
* **Hugging Face Transformers** (`bert-base`, `deberta-v3-base`, or `resume-ner` models)
* **spaCy** (optional, for rule-based improvements)
* **Regex** for GPA, phone numbers, emails

---

## ⚙️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/IzzieIM/cv--Parser-aggregator.git
cd cv-parser
pip install -r requirements.txt
```

---

## 🚀 Usage

### 1. Extract entities using pretrained model

```python
from transformers import pipeline

ner_pipeline = pipeline("ner", model="quantumiracle/bert-base-finetuned-resume-ner", aggregation_strategy="simple")

text = open("resume.txt", "r").read()
entities = ner_pipeline(text)
print(entities)
```

### 2. Extract GPA, Emails, Phone Numbers with Regex

```python
import re

def extract_email(text):
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

def extract_phone(text):
    return re.findall(r"\+?\d{10,15}", text)

def extract_gpa(text):
    return re.findall(r"\b\d{1,2}(\.\d{1,2})?\s*(?:GPA|CGPA|/10|/4|%)\b", text)
```

### 3. Combine into JSON

```python
parsed_cv = {
    "name": "Anusha Nikam",
    "email": extract_email(text),
    "contact": extract_phone(text),
    "education": [
        {"institute": "IIT Kharagpur", "gpa": "8.0/10"}
    ],
    "work_experience": [
        {"company": "Deloitte", "role": "Intern", "duration": "Jan 2025 - May 2025"}
    ],
    "projects": ["Deepfake Identification App", "Crypto Exchange Web App"],
    "skills": ["Python", "Machine Learning", "DSA"]
}

print(parsed_cv)
```

---

## 📂 Example Output

```json
{
  "name": "Anusha Nikam",
  "email": ["anusha@example.com"],
  "contact": ["+91-9876543210"],
  "education": [
    {"institute": "IIT Kharagpur", "gpa": "8.0/10"}
  ],
  "work_experience": [
    {"company": "Deloitte", "role": "Intern", "duration": "Jan 2025 - May 2025"}
  ],
  "projects": [
    "Deepfake Identification App",
    "Crypto Exchange Web App"
  ],
  "skills": ["Python", "Machine Learning", "DSA"]
}
```

---

## 🔮 Future Improvements

* Fine-tune NER model for more accurate **education & GPA linking**
* Add support for **multilingual resumes**
* Web API using **FastAPI/Flask**

---
