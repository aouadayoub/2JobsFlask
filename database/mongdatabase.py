from pymongo import MongoClient
from decouple import config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_jobs_collection():
    try:
        MONGO_URI = config('MONGO_URI')
        DATABASE_NAME = config('DATABASE_NAME')
        COLLECTION_NAME = config('COLLECTION_NAME')
        
        client = MongoClient(MONGO_URI)
        database = client[DATABASE_NAME]
        jobs_collection = database[COLLECTION_NAME]
        logger.info("Connected to MongoDB successfully")
        return jobs_collection
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise
