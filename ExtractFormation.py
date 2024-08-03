from langchain_together import Together
from decouple import config
import os

import ExtractDataOCR
import ExtractDataPyPDF2


def GetFormationResume(path):

    # Load environment variables
    together_api_key = config("together_api_key")
    os.environ["together_api_key"] = together_api_key

    llm = Together(
        model="togethercomputer/llama-2-70b-chat",
        temperature=0.7,
        max_tokens=128,
        top_k=1,
        together_api_key=together_api_key
    )

    # Context = ExtractDataOCR.extract_text_from_pdf(path)
    Context = ExtractDataPyPDF2.Extract_text_pypdf2(path)


    # print(Context)

    Prompt = f"""system

You are an expert in HR. Your goal is to analyze resumes and extract "Formations" (Education) from them.

user

Here is the context of a resume: '{Context}'.

Please extract all "Formations" and all details like (Date, school, and city) from this resume.

assistant

Make sure to extract a list of all "Formations" mentioned.
Make sure to extract only the formations, not experiences.

#FORMATIONS:
"""

    # print(Prompt)

    return llm(Prompt)


# PATH_FILE = "D:\HAMZA M2\Fati_CV.pdf"
# Answer = GetFormationResume(PATH_FILE)

# print(Answer)
"""PATH_FILE = r"C:\Users\aouad\OneDrive\Bureau\stage_ine2\projet_emplois\Extract-data-from-resume-using-LLMs\AOUAD_AYOUB_CV.pdf"
Answer = GetFormationResume(PATH_FILE)

print(Answer)"""