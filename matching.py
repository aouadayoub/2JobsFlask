import pymongo

# MongoDB client setup
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["job_database"]
jobs_collection = db["jobs"]

def MatchJobs(cv_skills, prompt_requirements):
    matched_jobs = []
    for job in jobs_collection.find():
        job_skills = job.get('skills', [])
        if all(skill in job_skills for skill in cv_skills) and all(req in job_skills for req in prompt_requirements):
            matched_jobs.append(job)
    return matched_jobs
