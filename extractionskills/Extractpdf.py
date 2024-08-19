import pdfplumber

def extract_text_pdfplumber(path_file):
    # Open the PDF file
    with pdfplumber.open(path_file) as pdf:
        # List to store the content of all pages
        content = []

        # Extract text from each page
        for page in pdf.pages:
            content.append(page.extract_text())

    return content

# Path to your PDF files
#PATH_FILE_SCANED = r"C:\Users\aouad\OneDrive\Bureau\stage_ine2\Convention_aouad_ayoub.pdf"
#PATH_FILE_NORMAL = r"C:\Users\aouad\OneDrive\Bureau\cv\AOUAD_AYOUB_CV.pdf

# Example usage
#content = extract_text_pdfplumber(PATH_FILE_NORMAL)
#content = extract_text_pdfplumber(PATH_FILE_NORMAL)
#print(content)