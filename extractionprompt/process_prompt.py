from langchain_together import Together
from decouple import config
from langchain_core.messages import HumanMessage
import redis
import os
import hashlib
import json

# Configure Redis connection using environment variable
redis_client = redis.StrictRedis.from_url(config("REDIS_URL"), decode_responses=True)

def generate_cache_key(prompt):
    """Generate a unique cache key based on the prompt."""
    return hashlib.md5(prompt.encode('utf-8')).hexdigest()

def ProcessPrompt(prompt):
    cache_key = generate_cache_key(prompt)
    
    # Check if result is in the Redis cache
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    together_api_key = config("together_api_key")
    os.environ["together_api_key"] = together_api_key

    llm = Together(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        temperature=0.7,
        max_tokens=512,
        top_k=1,
        together_api_key=together_api_key
    )

    Prompt = f"""system
You are an expert HR AI assistant.
Please analyze the following prompt and extract the job title the user is looking for:

{prompt}

Follow these guidelines:
1. Extract ONLY the job title explicitly mentioned in the prompt.
2. Format the output as a single job title without additional text.
3. Support both English and French prompts.
4. If the job title in the prompt is in a language other than English, translate it to English.

Example output:
Data Analyst
Project Manager
Software Engineer
Financial Analyst
Customer Relationship Manager
Supply Chain Manager
Sales Manager
Technical Writer
Line Cook 

Here is the job title extracted from the prompt:

"""

    message = HumanMessage(content=Prompt)
    response = llm.invoke([message]).strip()

    # Cache the result in Redis
    redis_client.set(cache_key, json.dumps(response), ex=3600)  # Cache expires in 1 hour

    return response.strip()


"""# Example usage
if __name__ == "__main__":
    prompt = 'i am looking for a line cook position'
    answer = ProcessPrompt(prompt)
    print(answer)
"""