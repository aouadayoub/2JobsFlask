from langchain_together import Together
from decouple import config
from langchain_core.messages import HumanMessage
import os

#import ExtractDataOCR
#import ExtractDataPyPDF2
import testpdf

def GetSkillsResume(path):
    # Load environment variables
    together_api_key = config("together_api_key")
    os.environ["together_api_key"] = together_api_key

    llm = Together(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        temperature=0.7,
        max_tokens=512,
        top_k=1,
        together_api_key=together_api_key
    )

    # Context = ExtractDataOCR.extract_text_from_pdf(path)
    Context = testpdf.extract_text_pdfplumber(path)

    Prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an expert HR AI assistant specialized in analyzing resumes from various professional fields and extracting relevant skills.<|eot_id|><|start_header_id|>user<|end_header_id|>
Please analyze the following resume and extract only the professional and technical skills mentioned:

{Context}

Follow these guidelines:
1. Extract ONLY professional and technical skills explicitly mentioned in the resume.
2. Include skills relevant to any job sector, not just IT.
3. DO NOT include: languages spoken/written, projects, work experiences, personal qualities, soft skills, certifications, qualifications, or education details.
4. Focus on specific tools, technologies, methodologies, and professional competencies relevant to the person's field.
5. Format the output as a bullet point list of skills only, without additional text.
6. Support both English and French skills.

Example output for various fields:
• Data Analysis
• Project Management
• AutoCAD
• Financial Modeling
• Customer Relationship Management
• Gestion de la chaîne d'approvisionnement
• Techniques de vente
• Rédaction technique<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Here is the list of professional and technical skills extracted from the resume:

"""

    message = HumanMessage(content=Prompt)
    response = llm.invoke([message])
    return response

#PATH_FILE = r"C:\Users\aouad\OneDrive\Bureau\cv\FR_CV_AHIDAR_SAMI.pdf.pdf"
#PATH_FILE = r"C:\Users\aouad\OneDrive\Bureau\cv\AJMAL CV .pdf"
#PATH_FILE = r"C:\Users\aouad\Downloads\CV_TEMPLATE_0003.pdf"
#skills = GetSkillsResume(PATH_FILE)
#print(skills)
#skills + matching code 