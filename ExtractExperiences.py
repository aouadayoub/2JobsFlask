from langchain_community.llms import Together
from decouple import config
import os

import ExtractDataOCR
import ExtractDataPyPDF2




def GetEXperiencesResume(path):

    # Load environment variables
    together_api_key = config("together_api_key")
    os.environ["together_api_key"] = together_api_key

    llm = Together(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        temperature=0.7,
        max_tokens=128,
        top_k=1,
        together_api_key=together_api_key
    )

    # Context = ExtractDataOCR.extract_text_from_pdf(path)
    Context = ExtractDataPyPDF2.Extract_text_pypdf2(path)

    Prompt = f"""system

You are an expert in HR. Your goal is to analyze resumes and extract "Expériences Professionnelles" (Professional Experiences) from them.

user

Here is the context of a resume: '{Context}'.

Please extract all "Expériences Professionnelles" (Professional Experiences) from this resume.

assistant

Make sure to extract a list of only "Expériences Professionnelles" (Professional Experiences) and not projects or skills.

#EXPERIENCES:
"""

    return llm(Prompt)


"""PATH_FILE = r"C:\Users\aouad\OneDrive\Bureau\stage_ine2\projet_emplois\Extract-data-from-resume-using-LLMs\AOUAD_AYOUB_CV.pdf"
Answer = GetEXperiencesResume(PATH_FILE)

print(Answer)"""