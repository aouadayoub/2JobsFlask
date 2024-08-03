# Requirements:

# Before we start, make sure you have the following libraries installed:
    # 1. pdf2image: To convert PDF files into images. "pip install pdf2image"
    # 2. pytesseract: A Python wrapper for Google's Tesseract OCR engine. "pip install pytesseract"
    # 3. OpenCV: For image preprocessing tasks like deskewing and grayscale conversion. "pip install opencv-python"
    # 4. pandas: For storing extracted text data in a structured manner. "pip install pandas"

# Attention: the libraries convert_from_path and tesseract require additional packages.
# For convert_from_path, you need to install poppler. You can follow this link to know how to install it:
# "https://www.youtube.com/watch?v=SioLV0f0sr0&t=11s&ab_channel=CodingDiksha"
# For tesseract, you need to install tesseract. You can follow this link to know how:
# "https://www.youtube.com/watch?v=LMM6s9JL5GA&ab_channel=datascienceAnywhere"

from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np
import os

# Function for preprocessing images
def deskew(image):
    if not isinstance(image, np.ndarray):
        raise ValueError("Input image is not a valid numpy array")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

# Function for extracting text from images
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(PATH_FILE):
    # Function to transform images into text
    pages = convert_from_path(PATH_FILE, poppler_path=r'C:\poppler\Library\bin')

    # Create a directory to store the images if it doesn't exist
    output_directory = 'test/img'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Save the images of the PDF pages in a directory
    for i, page in enumerate(pages):
        page.save(os.path.join(output_directory, 'page'+str(i)+'.jpg'), 'JPEG')

    extract_text = []
    for page in pages:
        # Step 2: Preprocess the image (deskew)
        preprocess_image = deskew(np.array(page))

        # Step 3: Extract text using OCR
        text = extract_text_from_image(preprocess_image)

        # Step 4: Add text page into list
        extract_text.append(text)

    return extract_text

# Usage of the function extract_text_from_pdf
#PATH_FILE = r"C:\Users\aouad\AOUAD_AYOUB_CV.pdf"
#PATH_FILE = r"C:\Users\aouad\AOUAD_AYOUB_CV_scanned.pdf"
#extracted_text = extract_text_from_pdf(PATH_FILE)
#print(extracted_text)