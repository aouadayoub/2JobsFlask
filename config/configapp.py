import os
from decouple import config
from matching.matching_json import load_jobs_from_json, build_job_index


def configureApp(app):
    # Set the path for the uploads folder and other configuration
    UPLOAD_FOLDER = config('UPLOAD_FOLDER')
    app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', UPLOAD_FOLDER))
    
    # Ensure JOB_JSON_PATH is correctly relative to the root of the project
    JOB_JSON_PATH = config('JOB_JSON_PATH')
    app.config['JOB_JSON_PATH'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', JOB_JSON_PATH))

    
def initializeData(app):
    # Load job data and build job index once at startup
    jobs = load_jobs_from_json(app.config['JOB_JSON_PATH'])
    job_index = build_job_index(jobs)
    return jobs, job_index
