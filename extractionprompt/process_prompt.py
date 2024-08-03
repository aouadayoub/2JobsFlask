from langchain_together import Together
from decouple import config
from langchain_core.messages import HumanMessage
from functools import lru_cache
import os



@lru_cache(maxsize=128)
def ProcessPrompt(prompt):
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
You are an expert HR AI assistant.user
Please analyze the following prompt and extract the job title the user is looking for:

{prompt}

Follow these guidelines:
1. Extract ONLY the job title explicitly mentioned in the prompt.
2. Format the output as a single job title without additional text.
3. Support both English and French prompts.

Example output:
• Data Analyst
• Project Manager
• Software Engineer
• Financial Analyst
• Customer Relationship Manager
• Supply Chain Manager
• Sales Manager
• Technical Writerassistant

Here is the job title extracted from the prompt:

"""

    message = HumanMessage(content=Prompt)
    response = llm.invoke([message])
    return response.strip()

def clean_job_title(job_title):
    """
    Clean the job title by removing unwanted characters and bullet points.
    """
    job_title = job_title.replace("•", "").strip()
    return job_title
#prompt='I am looking for an opprotunity in cooking'
#answer=ProcessPrompt(prompt)
#print(answer)