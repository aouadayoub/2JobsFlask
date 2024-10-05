from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from extractionskills.ExtractSkills import GetSkillsResume
from extractionprompt.process_prompt import ProcessPrompt
from matching.matching import match_jobs  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:4000", "https://twojobsbackend.onrender.com"]}}, supports_credentials=True)

# Set the path for the uploads folder and other configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../upload')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/process", methods=["POST"])
def process():
    data = request.json

    # Retrieve values from JSON
    cv_filename = data.get("cv_filename")
    prompt = data.get("prompt")
    country = data.get("country")

    if not cv_filename or not prompt or not country:
        return jsonify({"error": "Missing CV filename, prompt, or country"}), 400

    # Construct the full path
    cv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)

    # Check if the path is valid and file exists
    if not os.path.exists(cv_file_path):
        return jsonify({"error": "File does not exist"}), 400

    try:
        # Process the CV file
        cv_skills = GetSkillsResume(cv_file_path)
        job_title = ProcessPrompt(prompt)

        # Call the match_jobs function
        matched_jobs = match_jobs(cv_skills, job_title, country)

        return jsonify({"matched_jobs": matched_jobs, "job_title": job_title, "country": country})

    except Exception as e:
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=4000)
    
