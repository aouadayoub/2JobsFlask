import ExtractData

import streamlit as st
import os


def generate_quiz():
    # Generate question and answer
    question = "This is a sample question?"
    answer = "This is the sample answer."

    # Explanation message
    explanation = "Do you know the answer?"

    return question, answer, explanation


def main():

    # sessions initialisation
    if "FILE_PATH" not in st.session_state:
        st.session_state.FILE_PATH = None

    # Define File_Text as a global variable outside of any function scope
    File_Text = None
    
    st.set_page_config("Fist QuizBot")
    st.title("Your PDF 📖 to amazing Game")

    with st.sidebar:

        st.header("Extract Information from CV")
        st.subheader("Upload your CV 📖")
        
        pdf_file = st.file_uploader("upload your pdf file and start process")
        if st.button("Generate Information"):
            st.spinner("Processing")

            if pdf_file:
                # Extract file path from uploaded file object
                st.session_state.FILE_PATH = os.path.join(pdf_file.name)
                with open(st.session_state.FILE_PATH, "wb") as f:
                    f.write(pdf_file.read())


    if st.session_state.FILE_PATH is not None:

        formation, experiences, skills = ExtractData.ExtractData(st.session_state.FILE_PATH)

        st.write(formation)

        st.write(experiences)

        st.write(skills)
            




if __name__ == "__main__":
    main()