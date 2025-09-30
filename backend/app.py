from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
from werkzeug.utils import secure_filename
from pathlib import Path

# base NLP model
from nlp_model import extract_details_from_file  

# other extractors
from certificate_extracter import extract_certifications
from dob_location_language_extractor import extract_dob, extract_location, extract_languages
from linkedin_website_extractor import extract_linkedin, extract_websites
from misc_extractor import extract_is_resume_probability, extract_redacted_text
from objective_proffession_summary_extractor import extract_objective, extract_profession, extract_summary
from publications_reference_extractor import extract_publications, extract_referees
from work_experience import extract_total_experience, extract_work_experience

# Configuration
UPLOAD_FOLDER = 'uploads'
PARSED_FOLDER = 'parsed_data'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PARSED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Backend is running"}), 200

@app.route('/api/parse-cv', methods=['POST'])
def parse_cv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Allowed: pdf, docx, pptx, txt"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # --- Step 1: Run base extractor ---
        parsed_data = extract_details_from_file(filepath)

        # --- Step 2: Load raw text for other extractors ---
        from nlp_model import load_text
        raw_text = load_text(Path(filepath))  # <-- FIXED HERE

        # --- Step 3: Call other extractors ---
        extra_data = {
            "certifications": extract_certifications(raw_text),
            "date_of_birth": extract_dob(raw_text),
            "location": extract_location(raw_text),
            "languages": extract_languages(raw_text),
            "linkedin": extract_linkedin(raw_text),
            "websites": extract_websites(raw_text),
            "is_resume_probability": extract_is_resume_probability(raw_text),
            "redacted_text": extract_redacted_text(raw_text),
            "objective": extract_objective(raw_text),
            "profession": extract_profession(raw_text),
            "summary": extract_summary(raw_text),
            "publications": extract_publications(raw_text),
            "referees": extract_referees(raw_text),
            "total_experience": extract_total_experience(raw_text),
            "work_experience": extract_work_experience(raw_text),
        }

        # --- Step 4: Merge all results ---
        parsed_data.update(extra_data)

        # Save JSON (optional)
        json_filename = filename.rsplit('.', 1)[0] + '.json'
        with open(os.path.join(PARSED_FOLDER, json_filename), 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=4)

        return jsonify({
            "message": "File parsed successfully",
            "filename": filename,
            "parsed_data": parsed_data
        }), 200

    except Exception as e:
        return jsonify({"error": f"Failed to parse file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)