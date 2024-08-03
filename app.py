from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from extractionskills.ExtractSkills import GetSkillsResume
from extractionprompt.process_prompt import ProcessPrompt, clean_job_title
from matching.matching_json import MatchJobs
from config.configapp import configureApp, initializeData

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:4000"}}, supports_credentials=True)

# Set the path for the uploads folder and other configuration
configureApp(app)

# Load job data and build job index once at startup
jobs, job_index = initializeData(app)


@app.route("/process", methods=["POST"])
def process():
    data = request.json

    # Retrieve values from JSON
    cv_filename = data.get("cv_filename")
    prompt = data.get("prompt")
    country = data.get("country")

    if not cv_filename or not prompt or not country:
        logger.error("Missing CV filename, prompt, or country")
        return jsonify({"error": "Missing CV filename, prompt, or country"}), 400

    # Construct the full path
    cv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], cv_filename)

    # Check if the path is valid and file exists
    if not os.path.exists(cv_file_path):
        logger.error("File does not exist")
        return jsonify({"error": "File does not exist"}), 400

    try:
        # Process the CV file
        cv_skills = GetSkillsResume(cv_file_path)
        job_title = ProcessPrompt(prompt).strip()
        cleaned_job_title = clean_job_title(job_title)  # Clean the job title
        prompt_requirements = [cleaned_job_title]

        matched_job_ids = MatchJobs(cv_skills, prompt_requirements, job_index, country, jobs)
        matched_jobs = [job for job in jobs if job['id'] in matched_job_ids]

        return jsonify({"matched_jobs": matched_jobs, "job_title": cleaned_job_title, "country": country})

    except Exception as e:
        logger.error(f"Processing error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Processing error: {str(e)}"}), 500


if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=4000)
