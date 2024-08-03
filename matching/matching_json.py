import json
from collections import defaultdict
from functools import lru_cache
import os

@lru_cache(maxsize=1)
def load_jobs_from_json(json_path):
    """
    Load job data from a JSON file. Only load once and use caching if applicable.
    """
    if not os.path.isabs(json_path):
        # Construct absolute path if a relative path is provided
        json_path = os.path.join(os.path.dirname(__file__), json_path)
    with open(json_path, 'r') as f:
        return json.load(f)

def build_job_index(jobs):
    """
    Create an index for jobs based on their titles.
    """
    job_index = defaultdict(set)
    for job in jobs:
        job_id = job.get('id')
        if job_id is None:
            raise ValueError("Jobs must have a unique 'id' for indexing.")
        job_title = job.get('title', '').lower()
        job_index[job_title].add(job_id)
    return job_index

def MatchJobs(cv_skills, prompt_requirements, job_index, country, jobs):
    """
    Match jobs based on prompt requirements and country.
    """
    matched_jobs = set()
    for req in prompt_requirements:
        req_lower = req.lower()
        if req_lower in job_index:
            matched_jobs.update(job_index[req_lower])
    
    # Filter by country
    matched_jobs = [job_id for job_id in matched_jobs if is_job_in_country(job_id, country, jobs)]
    
    return matched_jobs

def is_job_in_country(job_id, country, jobs):
    """
    Check if the job with the given ID is in the specified country.
    """
    job = next((job for job in jobs if job['id'] == job_id), None)
    if job and job.get('country', '').lower() == country.lower():
        return True
    return False

# Example usage
"""if __name__ == "__main__":
    json_path = "jobs_data.json"  # Ensure this is the correct relative path
    jobs = load_jobs_from_json(json_path)
    job_index = build_job_index(jobs)

    cv_skills = ["Python", "Machine Learning"]
    prompt_requirements = ["cook"]
    country = "Canada"
    matched_jobs_ids = MatchJobs(cv_skills, prompt_requirements, job_index, country, jobs)
    matched_jobs = [job for job in jobs if job['id'] in matched_jobs_ids]
    print(matched_jobs)"""
