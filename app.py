import streamlit as st
from images import image_proc
from data import data_proc
from audio import process_audio
from text_regex import text_regex


def main():
    st.header("Select File")
    # Upload image or audio based on the selected file type

    file_type = st.selectbox("", ("Image", "Audio", "Tabular","Regex Manipulation"))

    if file_type == "Image":
        uploaded_file = st.file_uploader(label="Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image_proc(uploaded_file)

    elif file_type == "Audio":
        uploaded_file = st.file_uploader(label="Choose an audio file...", type=["mp3", "wav"])
        if uploaded_file is not None:
            process_audio(uploaded_file)

    elif file_type == "Tabular":
        uploaded_file = st.file_uploader(label="Choose a CSV or Excel file", type=["csv", "xlsx"])
        # Data processing section
        if uploaded_file is not None:
            data_proc(uploaded_file)
        
    elif file_type == "Regex Manipulation":
        # Data processing section
        text_regex()
    
    
if __name__ == "__main__":
    main()
