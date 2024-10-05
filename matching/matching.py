from database.mongdatabase import get_jobs_collection
import redis
import logging
from decouple import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to Redis
redis_client = redis.StrictRedis.from_url(config('REDIS_URL'))

def match_jobs(cv_skills, job_title, country=None, limit=150):
    # Create a unique cache key based on the function parameters
    cache_key = f"matched_jobs:{cv_skills}:{job_title}:{country}:{limit}"

    # Check if the result is in Redis cache
    cached_result = redis_client.get(cache_key)
    if cached_result:
        logger.info("Using cached results from Redis")
        return cached_result.decode('utf-8')  # Return cached result

    jobs_collection = get_jobs_collection()

    try:
        # Initialize query components
        queries = []
        
        # Match by job title
        if job_title:
            queries.append({'title': {'$regex': job_title, '$options': 'i'}})
        
        # Match by country if provided
        if country:
            queries.append({'country': country})
        
        # Match by skills if provided
        if cv_skills is not None:
            queries.append({
                '$or': [
                    {'skills': {'$exists': False}},  # Match if skills field does not exist
                    {'skills': {'$all': []}}         # Match if skills field is an empty array
                ]
            })
        
        # Build the aggregation pipeline
        aggregation_pipeline = []
        
        if queries:
            # Use $match stage to filter documents
            aggregation_pipeline.append({'$match': {'$and': queries}})
        
        # Add sorting stage to order by date (newest first)
        aggregation_pipeline.append({'$sort': {'date': -1}})
        
        # Add projection stage to include necessary fields (excluding _id)
        aggregation_pipeline.append({
            '$project': {
                '_id': 0,  # Exclude _id from the result
                'title': 1, 'skills': 1, 'company': 1, 'country': 1, 'job_link': 1, 'date': 1, 'location': 1, 'salary': 1, 'logo': 1, 'source': 1, 'business': 1
            }
        })
        
        # Apply limit to the results
        aggregation_pipeline.append({'$limit': limit})

        # Execute the aggregation pipeline
        cursor = jobs_collection.aggregate(aggregation_pipeline)
        matched_jobs = list(cursor)

        # Convert ObjectId to string for JSON serialization
        for job in matched_jobs:
            if '_id' in job:
                job['_id'] = str(job['_id'])

        logger.info(f"Matched {len(matched_jobs)} jobs.")

        # Store the result in Redis cache for future requests
        redis_client.set(cache_key, str(matched_jobs), ex=3600)  # Cache for 1 hour (3600 seconds)

    except Exception as e:
        logger.error(f"Error matching jobs: {str(e)}")
        matched_jobs = []

    return matched_jobs


"""# Example usage
if __name__ == "__main__":
    cv_skills = []
    job_title = "Line Cook"
    country = "Canada"
    matched_jobs = match_jobs(cv_skills, job_title, country)
    print("Matched Jobs:", matched_jobs)
"""